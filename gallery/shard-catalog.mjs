// Offline conversion only. Writes a fresh output directory; never changes input pins.
import {readFile,writeFile,mkdir,readdir,lstat} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {PUBLIC_FILES} from './build.mjs';
import {createHash} from 'node:crypto';
import {validateCatalog} from '../docs/core.mjs';
import {validateCatalogIndex,METADATA_LIMIT} from '../docs/core-catalog-v2.mjs';
export function splitCatalog(c){validateCatalog(c);const groups=new Map(),files=new Map(),shards=[];
 for(const asset of c.assets){if(!groups.has(asset.theme))groups.set(asset.theme,[]);groups.get(asset.theme).push(asset);}
 const encode=(theme,assets)=>Buffer.from(JSON.stringify({schemaVersion:2,theme,assets})+'\n');
 const emit=(theme,assets)=>{const bytes=encode(theme,assets);if(bytes.length>METADATA_LIMIT)throw Error('Single asset exceeds metadata budget');const sha256=createHash('sha256').update(bytes).digest('hex'),path=`metadata/${sha256}.json`;files.set(path,bytes);shards.push({theme,count:assets.length,path,size:bytes.length,sha256});};
 for(const [theme,assets]of groups){let page=[];for(const asset of assets){if(page.length&&encode(theme,[...page,asset]).length>METADATA_LIMIT){emit(theme,page);page=[];}page.push(asset);}if(page.length)emit(theme,page);}
 const {assets,...header}=c;const index={...header,schemaVersion:2,assetCount:assets.length,shards};validateCatalogIndex(index);const bytes=Buffer.from(JSON.stringify(index,null,2)+'\n');if(bytes.length>METADATA_LIMIT)throw Error('Index exceeds metadata budget');files.set('catalog-v2.json',bytes);return {index,files};
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const [input,out,legacy=input,retained=fileURLToPath(new URL('../docs/metadata',import.meta.url))]=process.argv.slice(2);if(!input||!out)throw Error('Usage: node gallery/shard-catalog.mjs <latest-v1-input> <new-directory> [frozen-legacy-v1] [retained-shards-directory]');
 const result=splitCatalog(JSON.parse(await readFile(input,'utf8'))),legacyBytes=await readFile(legacy);validateCatalog(JSON.parse(legacyBytes));
 if(legacyBytes.length>METADATA_LIMIT)throw Error('Legacy catalog exceeds 256 KiB; provide the frozen migration snapshot');
 const totalMetadataBytes=[...result.files.values()].reduce((n,b)=>n+b.length,0);let runtimeBytes=0;for(const name of PUBLIC_FILES.filter(n=>n!=='catalog.json'))runtimeBytes+=(await readFile(new URL('../docs/'+name,import.meta.url))).length;
 let retainedOldShardBytes=0,retainedOldShardCount=0,names=[];try{names=await readdir(retained);}catch(error){if(error.code!=='ENOENT')throw error;}for(const name of names){if(!/^[a-f0-9]{64}[.]json$/.test(name))throw Error('Unexpected retained shard');const path=join(retained,name),stat=await lstat(path);if(!stat.isFile()||stat.isSymbolicLink()||stat.size>METADATA_LIMIT)throw Error('Invalid retained shard');const bytes=await readFile(path);if(createHash('sha256').update(bytes).digest('hex')!==name.slice(0,64))throw Error('Retained shard integrity mismatch');if(!result.files.has('metadata/'+name)){retainedOldShardBytes+=bytes.length;retainedOldShardCount++;}}
 const projectedPagesBytes=totalMetadataBytes+legacyBytes.length+runtimeBytes+retainedOldShardBytes;
 const report={assets:result.index.assetCount,shards:result.index.shards.length,indexBytes:result.files.get('catalog-v2.json').length,totalMetadataBytes,legacyCatalogBytes:legacyBytes.length,runtimeBytes,retainedOldShardCount,retainedOldShardBytes,projectedPagesBytes,remainingBytes:1048576-projectedPagesBytes,pagesBudgetBytes:1048576,warning:projectedPagesBytes>=838860?'Exceeds 80% of Pages budget including retained shards':null,note:'Retained bytes measured from supplied/default directory; assemble package and run build --check before publication'};
 console.log(JSON.stringify(report));if(projectedPagesBytes>1048576)throw Error('Projected package exceeds unchanged 1 MiB Pages budget');
 await mkdir(out);if(result.index.shards.length)await mkdir(join(out,'metadata'));for(const [path,bytes]of result.files)await writeFile(join(out,path),bytes);
}
