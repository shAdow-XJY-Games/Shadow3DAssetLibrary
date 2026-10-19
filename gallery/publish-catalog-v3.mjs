// Read-only/offline publication planning. The sole writer owns journals, Git calls and CAS.
import {createHash} from 'node:crypto';import {readFile,writeFile,mkdir} from 'node:fs/promises';import {resolve,join,dirname} from 'node:path';import {fileURLToPath} from 'node:url';
import {buildPagedCatalog,pinPagedCatalog,auditPagedCatalog,appendCatalog,canonicalCatalog} from './catalog-v3.mjs';
import {SOURCE,assetSource,rawURL,validateCatalog} from '../docs/core.mjs';
const assert=(ok,message)=>{if(!ok)throw Error(message);};
const encode=value=>Buffer.from(JSON.stringify(value)+'\n');
export const contentIdentity=bytes=>({bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),git_blob_sha1:createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${bytes.length}\0`),bytes])).digest('hex')});
export function treeMap(tree){assert(tree&&!tree.truncated&&Array.isArray(tree.tree),'Complete immutable Git tree required');const map=new Map();for(const entry of tree.tree){assert(typeof entry.path==='string'&&!map.has(entry.path),'Duplicate tree path');map.set(entry.path,entry);}return map;}
export function unchangedCatalogProof(beforeInput,afterInput){
 const before=canonicalCatalog(beforeInput),after=canonicalCatalog(afterInput);assert(after.assets.length>=before.assets.length,'Old assets removed');let urls=0;
 for(let i=0;i<before.assets.length;i++){const old=before.assets[i],current=after.assets[i];assert(JSON.stringify(old)===JSON.stringify(current),'Old record/order changed: '+old.id);assert(JSON.stringify(assetSource(before,old))===JSON.stringify(assetSource(after,current)),'Old source changed: '+old.id);for(const file of Object.values(old.files)){assert(rawURL(assetSource(before,old),file.path)===rawURL(assetSource(after,current),file.path),'Old role URL changed');urls++;}}
 assert(JSON.stringify(before.source)===JSON.stringify(after.source),'Default source changed');for(const [id,source]of Object.entries(before.sources||{}))assert(JSON.stringify(source)===JSON.stringify(after.sources?.[id]),'Old source ID changed');assert(JSON.stringify(before.collection)===JSON.stringify(after.collection),'Collection changed');
 return {oldRecords:before.assets.length,oldRoleURLs:urls,oldSources:Object.keys(before.sources||{}).length,oldRecordsSourcesOrderAndURLsUnchanged:true};
}
export async function approvedAssetAddition(rows,{sourceId,assetCommit}){
 assert(Array.isArray(rows)&&rows.length===5,'Exactly five approved core files required');assert(/^[a-z0-9-]+$/.test(sourceId)&&/^[a-f0-9]{40}$/.test(assetCommit)&&!/^0{40}$/.test(assetCommit),'Invalid new source pin');
 const metadataRow=rows.find(row=>row.repo_path.endsWith('/metadata.json'));assert(metadataRow,'Missing approved metadata file');
 const bytes=await readFile(metadataRow.local_path),metadata=JSON.parse(bytes),record={...metadata,sourceId},source={...SOURCE,commit:assetCommit};validateCatalog({schemaVersion:1,sources:{[sourceId]:source},assets:[record]});
 const paths=new Map(rows.map(row=>[row.repo_path,row]));assert(paths.size===5,'Duplicate approved core path');
 for(const file of Object.values(record.files)){const row=paths.get(file.path);assert(row&&row.bytes===file.size&&row.sha256===file.sha256,'Record differs from approved core file');}
 assert(Object.keys(record.files).length===4,'Five-core adapter requires the four original file roles plus metadata');
 for(const row of rows){const body=row===metadataRow?bytes:await readFile(row.local_path),identity=contentIdentity(body);assert(identity.bytes===row.bytes&&identity.sha256===row.sha256&&identity.git_blob_sha1===row.git_blob_sha1,'Approved core bytes changed: '+row.repo_path);}
 return {assets:[record],sources:{[sourceId]:source}};
}
export function planGraphPublication({before,addition,baseTree}){
 const base=treeMap(baseTree),after=addition?appendCatalog(before,addition):canonicalCatalog(before),proof=unchangedCatalogProof(before,after),built=buildPagedCatalog(after),changes=[],allNodes=[];
 for(const [path,bytes]of built.files){const identity=contentIdentity(bytes),row={path,...identity},existing=base.get(path);if(existing){assert(existing.type==='blob'&&existing.mode==='100644'&&existing.sha===row.git_blob_sha1&&existing.size===row.bytes,'Content-addressed graph path collision: '+path);}else changes.push(row);allNodes.push(row);}
 const protectedLegacy=[...base.values()].filter(entry=>entry.type==='blob'&&(entry.path==='docs/catalog.json'||entry.path==='docs/catalog-v2.json'||entry.path.startsWith('docs/metadata/')||entry.path==='docs/app.mjs'||entry.path==='docs/core-catalog-v2.mjs')).map(entry=>({path:entry.path,sha:entry.sha,size:entry.size,mode:entry.mode}));
 return {...built,plan:{version:1,mode:addition?'append':'migration',baseTree:baseTree.sha,oldAssetCount:canonicalCatalog(before).assets.length,newAssetCount:after.assets.length,snapshot:built.template.snapshot,proof,graphChanges:changes,allNodes,graphReused:allNodes.length-changes.length,protectedLegacy,requiredProtocol:'Immutable asset commit (append only), immutable graph commit, then entry commit; one expected-main force=false CAS. Never use the old exact-seven/slice-last-two publisher.'}};
}
export function verifyExactTreeChanges(beforeTree,afterTree,manifest){
 const before=treeMap(beforeTree),after=treeMap(afterTree),expected=new Map(manifest.map(row=>[row.path,row]));assert(expected.size===manifest.length,'Duplicate manifest path');
 for(const [path,old]of before){const current=after.get(path);assert(current&&current.mode===old.mode&&current.type===old.type,'Deleted or changed old path: '+path);}
 const changed=[];
 for(const [path,current]of after){if(current.type!=='blob')continue;const old=before.get(path),row=expected.get(path);if(!old||old.sha!==current.sha){assert(row,'Unplanned changed blob: '+path);changed.push(path);}if(row)assert(current.sha===row.git_blob_sha1&&current.size===row.bytes&&current.mode==='100644','Planned blob identity mismatch: '+path);else assert(old&&current.sha===old.sha&&current.size===old.size,'Unplanned blob mutation: '+path);}
 assert(changed.length===expected.size&&changed.every(path=>expected.has(path)),'Exact change manifest mismatch');return {result:'PASS_EXACT_MANIFEST_NO_DELETIONS',oldPathsPreserved:before.size,changedBlobPaths:changed.sort()};
}
export function verifyCommitChain({baseline,assetCommit,graphCommit,entryCommit,root}){
 const check=(commit,parent)=>{assert(/^[a-f0-9]{40}$/.test(commit?.sha)&&commit.parents?.length===1&&commit.parents[0].sha===parent,'Immutable commit parent chain mismatch');};
 if(assetCommit)check(assetCommit,baseline);check(graphCommit,assetCommit?.sha||baseline);check(entryCommit,graphCommit.sha);assert(root.metadataSource.commit===graphCommit.sha,'Entry does not pin the verified graph commit');return {result:'PASS_IMMUTABLE_PARENT_CHAIN',baseline,asset:assetCommit?.sha||null,graph:graphCommit.sha,entry:entryCommit.sha};
}
export function verifyRemoteGraphTree(plan,tree){const map=treeMap(tree);for(const row of plan.allNodes){const node=map.get(row.path);assert(node?.type==='blob'&&node.mode==='100644'&&node.sha===row.git_blob_sha1&&node.size===row.bytes,'Remote graph node identity mismatch: '+row.path);}return {result:'PASS_ALL_IMMUTABLE_GRAPH_BLOB_IDENTITIES',nodes:plan.allNodes.length};}
export async function writePlan(plan,out){
 await mkdir(out);for(const row of plan.plan.graphChanges){await mkdir(dirname(join(out,row.path)),{recursive:true});await writeFile(join(out,row.path),plan.files.get(row.path));}
 await writeFile(join(out,'publication-plan.json'),encode(plan.plan));await writeFile(join(out,'catalog-v3.template.json'),encode(plan.template));await writeFile(join(out,'new-catalog-expanded.json'),encode(plan.catalog));await writeFile(join(out,'graph-report.json'),encode(plan.report));
}
export function finalizeEntry(template,graphCommit){const root=pinPagedCatalog(template,graphCommit),bytes=encode(root);return {root,bytes,manifest:[{path:'docs/catalog-v3.json',...contentIdentity(bytes)}]};}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const [command,...args]=process.argv.slice(2),read=async path=>JSON.parse(await readFile(path,'utf8'));
 if(command==='from-approved'){const [manifest,sourceId,assetCommit,output]=args;if(!manifest||!sourceId||!assetCommit||!output)throw Error('Usage: from-approved <approved-core-files.json> <source-id> <verified-asset-commit> <addition-output>');const addition=await approvedAssetAddition(await read(manifest),{sourceId,assetCommit});await writeFile(output,encode(addition));console.log(JSON.stringify({assetId:addition.assets[0].id,sourceId,assetCommit,approvedCoreFiles:5}));
 }else if(command==='prepare'){
  const [expanded,tree,out,additionFile]=args;if(!expanded||!tree||!out)throw Error('Usage: prepare <verified-current-expanded.json> <complete-base-tree.json> <fresh-output> [approved-addition.json]');
  const plan=planGraphPublication({before:await read(expanded),baseTree:await read(tree),...(additionFile?{addition:await read(additionFile)}:{})});await writePlan(plan,out);console.log(JSON.stringify({proof:plan.plan.proof,report:plan.report,newNodes:plan.plan.graphChanges.length,reusedNodes:plan.plan.graphReused}));
 }else if(command==='entry'){
  const [prepared,graphCommit]=args;if(!prepared||!graphCommit)throw Error('Usage: entry <prepared-directory> <verified-graph-commit>');const entry=finalizeEntry(await read(join(prepared,'catalog-v3.template.json')),graphCommit);await writeFile(join(prepared,'catalog-v3.json'),entry.bytes);await writeFile(join(prepared,'entry-manifest.json'),encode(entry.manifest));console.log(JSON.stringify(entry.manifest));
 }else if(command==='verify-tree'){
  const [before,after,manifest]=args;console.log(JSON.stringify(verifyExactTreeChanges(await read(before),await read(after),await read(manifest))));
 }else if(command==='verify-graph'){
  const [plan,tree]=args;console.log(JSON.stringify(verifyRemoteGraphTree(await read(plan),await read(tree))));
 }else throw Error('Expected from-approved, prepare, entry, verify-tree or verify-graph');
}
