// Dependency-free Pages packaging: an explicit allowlist prevents model duplication.
import {readFile,writeFile,mkdir,stat,readdir,lstat} from 'node:fs/promises';
import {resolve,dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {validateCatalog} from '../docs/core.mjs';
import {validateCatalogIndex,validateMetadataShard} from '../docs/core-catalog-v2.mjs';
export const PUBLIC_FILES=['index.html','style.css','app.mjs','core.mjs','viewer.mjs','core-catalog-v2.mjs','catalog.json','.nojekyll'];
const here=dirname(fileURLToPath(import.meta.url)),root=dirname(here),publicDir=join(root,'docs');
// Local packaging limits, not hosting-provider limits. Browser budgets remain unchanged.
export const ACTIVE_METADATA_BUDGET=1048576,HISTORY_BUDGET=8388608,SHELL_BUDGET=262144;
export const PACKAGE_BUDGET=ACTIVE_METADATA_BUDGET+HISTORY_BUDGET+SHELL_BUDGET;
export function assessBudget({activeMetadataBytes,historyBytes,shellBytes}){
 for(const n of [activeMetadataBytes,historyBytes,shellBytes])if(!Number.isSafeInteger(n)||n<0)throw Error('Invalid budget byte count');
 if(activeMetadataBytes>ACTIVE_METADATA_BUDGET)throw Error('Active metadata budget exceeds 1 MiB');
 if(historyBytes>HISTORY_BUDGET)throw Error('Historical metadata budget exceeds 8 MiB');
 if(shellBytes>SHELL_BUDGET)throw Error('Runtime and shell budget exceeds 256 KiB');
 const packageBytes=activeMetadataBytes+historyBytes+shellBytes;
 if(packageBytes>PACKAGE_BUDGET)throw Error('Local package budget exceeded');
 return {activeMetadataBytes,historyBytes,shellBytes,packageBytes,activeMetadataBudget:ACTIVE_METADATA_BUDGET,historyBudget:HISTORY_BUDGET,shellBudget:SHELL_BUDGET,packageBudget:PACKAGE_BUDGET,historyWarning:historyBytes>=HISTORY_BUDGET*0.75?'Historical metadata is at least 75% of local 8 MiB budget':null};
}
export function classifyBudget(index, sizes){
 const active=new Set(index.schemaVersion===2?['catalog-v2.json',...index.shards.map(s=>s.path)]:['catalog.json']);
 let activeMetadataBytes=0,historyBytes=0,shellBytes=0;
 for(const [path,size]of sizes){if(active.has(path))activeMetadataBytes+=size;else if(path==='catalog.json'||path.startsWith('metadata/'))historyBytes+=size;else shellBytes+=size;}
 return assessBudget({activeMetadataBytes,historyBytes,shellBytes});
}

async function readIndex(){const names=await readdir(publicDir);return validateCatalogIndex(JSON.parse(await readFile(join(publicDir,names.includes('catalog-v2.json')?'catalog-v2.json':'catalog.json'),'utf8')));}
export async function checkCatalog({verifyFiles=true}={}){
 const index=await readIndex();
 validateCatalog(JSON.parse(await readFile(join(publicDir,'catalog.json'),'utf8')));
 const assets=[];if(index.schemaVersion===2)for(const shard of index.shards){const file=join(publicDir,shard.path);if((await lstat(file)).isSymbolicLink())throw Error('Metadata symlink not allowed');const bytes=await readFile(file);if(bytes.length!==shard.size||createHash('sha256').update(bytes).digest('hex')!==shard.sha256)throw Error('Metadata integrity mismatch');assets.push(...validateMetadataShard(index,shard,JSON.parse(bytes)));}
 const c=index.schemaVersion===1?index:validateCatalog({...index,schemaVersion:1,assets});
 for(const a of c.assets){if(!['prop','modular','scene','character'].includes(a.assetKind))throw Error('Invalid assetKind');if(!/^\d+\.\d+\.\d+$/.test(a.version))throw Error('Invalid version');for(const k of ['category','theme','style','title'])if(typeof a[k]!=='string'||!a[k])throw Error('Missing '+k);if(!Number.isInteger(a.triangles)||a.triangles<1||a.triangles>100000)throw Error('Triangle budget exceeded');if(!Number.isInteger(a.materials)||a.materials<1||a.materials>64)throw Error('Material budget exceeded');for(const k of ['x','y','z'])if(!(Number.isFinite(a.bounds?.[k])&&a.bounds[k]>0))throw Error('Invalid bounds');if(a.bounds.unit!=='m')throw Error('Invalid units');
 const ext={glb:/\.glb$/,blend:/\.blend$/,generator:/\.py$/,render:/\.(png|jpg|jpeg|webp)$/,reference:/\.(png|jpg|jpeg|webp)$/};for(const [role,f]of Object.entries(a.files)){if(!ext[role]?.test(f.path))throw Error('Invalid role extension');const budget=role==='glb'?5242880:role==='render'||role==='reference'?2097152:role==='generator'?524288:26214400;if(f.size>budget)throw Error('File budget exceeded: '+f.path);if(verifyFiles){const file=join(root,f.path);if((await lstat(file)).isSymbolicLink())throw Error('Asset symlink not allowed');const bytes=await readFile(file);if(bytes.length!==f.size||createHash('sha256').update(bytes).digest('hex')!==f.sha256)throw Error('Asset integrity mismatch: '+f.path);}}
 }return c;
}
export function checkNoDeletions(base){if(!base)return;const removed=execFileSync('git',['diff','--name-only','--diff-filter=D',`${base}...HEAD`],{cwd:root,encoding:'utf8'}).trim();if(removed)throw Error('History protection: deleted tracked files require explicit review:\n'+removed);}
export async function publicFiles(){const index=await readIndex();if(index.schemaVersion===1)return [...PUBLIC_FILES];const paths=[];if(index.shards.length|| (await readdir(publicDir)).includes('metadata')){const dir=await lstat(join(publicDir,'metadata'));if(!dir.isDirectory()||dir.isSymbolicLink())throw Error('Invalid metadata directory');for(const name of await readdir(join(publicDir,'metadata'))){if(!/^[a-f0-9]{64}[.]json$/.test(name))throw Error('Unexpected metadata file');const path='metadata/'+name,s=await lstat(join(publicDir,path));if(!s.isFile()||s.isSymbolicLink()||s.size>262144)throw Error('Invalid metadata file');const bytes=await readFile(join(publicDir,path));if(createHash('sha256').update(bytes).digest('hex')!==name.slice(0,64))throw Error('Metadata integrity mismatch');const payload=JSON.parse(bytes);validateMetadataShard(index,{theme:payload.theme,count:payload.assets?.length},payload);paths.push(path);}}for(const shard of index.shards)if(!paths.includes(shard.path))throw Error('Missing metadata shard');return [...PUBLIC_FILES,'catalog-v2.json',...paths.sort()];}
export async function checkPublicDirectory(){const files=await publicFiles(),names=await readdir(publicDir);const allowed=[...PUBLIC_FILES,...(files.includes('catalog-v2.json')?['catalog-v2.json']:[]),...(files.some(n=>n.startsWith('metadata/'))?['metadata']:[])];if(names.length!==allowed.length||names.some(n=>!allowed.includes(n)))throw Error('docs/ must contain only the Pages allowlist');if(allowed.includes('metadata')){const dir=await lstat(join(publicDir,'metadata'));if(!dir.isDirectory()||dir.isSymbolicLink())throw Error('Invalid metadata directory');const actual=await readdir(join(publicDir,'metadata'));const expected=files.filter(n=>n.startsWith('metadata/')).map(n=>n.slice(9));if(actual.length!==expected.length||actual.some(n=>!expected.includes(n)))throw Error('Unexpected metadata file');}const sizes=new Map();let total=0;for(const n of files){const s=await lstat(join(publicDir,n));if(!s.isFile()||s.isSymbolicLink()||s.size>262144)throw Error('Invalid public file: '+n);total+=s.size;sizes.set(n,s.size);}const budget=classifyBudget(await readIndex(),sizes);if(budget.historyWarning)console.warn(budget.historyWarning);return budget.packageBytes;}
export async function build(out){await checkPublicDirectory();const files=await publicFiles(),target=resolve(out);if(target===root||target===here||target===publicDir||target.startsWith(root+'/assets'))throw Error('Unsafe output directory');await checkCatalog();checkNoDeletions(process.env.BASE_REF);await mkdir(target,{recursive:true});const existing=await readdir(target);if(existing.length)throw Error('Output contains unexpected files; use a fresh directory');let total=0;for(const name of files){const source=join(publicDir,name);if((await lstat(source)).isSymbolicLink())throw Error('Frontend symlink not allowed');const bytes=await readFile(source);if(bytes.length>262144)throw Error('Frontend per-file budget exceeded');total+=bytes.length;await mkdir(dirname(join(target,name)),{recursive:true});await writeFile(join(target,name),bytes);}if(total>PACKAGE_BUDGET)throw Error('Local package budget exceeded');console.log(`Pages package verified: ${files.length} files, ${total} bytes, no models or images copied.`);return {files:files.length,bytes:total};}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){if(process.argv[2]==='--check'){await checkCatalog();await checkPublicDirectory();checkNoDeletions(process.env.BASE_REF);console.log('Catalog integrity and docs allowlist verified.');}else{if(!process.argv[2])throw Error('Usage: node gallery/build.mjs --check | <fresh-output-directory>');await build(process.argv[2]);}}
