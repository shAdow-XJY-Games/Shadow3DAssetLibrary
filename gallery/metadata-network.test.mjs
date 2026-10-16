import test from'node:test';import assert from'node:assert/strict';import{createServer}from'node:http';import{gzipSync,brotliCompressSync}from'node:zlib';import{createHash}from'node:crypto';import{fetchVerifiedMetadata}from'../docs/core-catalog-v2.mjs';
const bytes=Buffer.from(JSON.stringify({example:'metadata '.repeat(500)})),sha256=createHash('sha256').update(bytes).digest('hex'),file={size:bytes.length,sha256,path:`metadata/${sha256}.json`};
test('real HTTP gzip and br decode before exact metadata size/hash validation',async()=>{let encoding='gzip';const server=createServer((req,res)=>{const compressed=encoding==='gzip'?gzipSync(bytes):brotliCompressSync(bytes);res.writeHead(200,{'Content-Encoding':encoding,'Content-Length':compressed.length});res.end(compressed);});await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));try{const base=`http://127.0.0.1:${server.address().port}/`;for(const value of ['gzip','br']){encoding=value;const actual=await fetchVerifiedMetadata(file,{fetcher:(path,options)=>fetch(new URL(path,base),options)});assert.deepEqual(Buffer.from(actual),bytes);}}finally{await new Promise(resolve=>server.close(resolve));}});
test('metadata supports no length header; rejects truncation, corruption and decoded expansion',async()=>{
 assert.deepEqual(Buffer.from(await fetchVerifiedMetadata(file,{fetcher:async()=>new Response(bytes)})),bytes);
 for(const body of [bytes.subarray(0,bytes.length-1),Buffer.alloc(bytes.length),Buffer.concat([bytes,Buffer.from('x')])])await assert.rejects(()=>fetchVerifiedMetadata(file,{fetcher:async()=>new Response(body,{headers:{'Content-Encoding':'gzip','Content-Length':'12'}})}));
 await assert.rejects(()=>fetchVerifiedMetadata(file,{fetcher:async()=>new Response(bytes,{headers:{'Content-Length':'12'}})}),/length mismatch/);
 let canceled=false;const body=new ReadableStream({start(controller){controller.enqueue(new Uint8Array(file.size+1));},cancel(){canceled=true;}});await assert.rejects(()=>fetchVerifiedMetadata(file,{fetcher:async()=>new Response(body,{headers:{'Content-Encoding':'br','Content-Length':'1'}})}),/exceeds expected/);assert.equal(canceled,true);
});

import{fetchCatalogEntry}from'../docs/core-catalog-v2.mjs';
const emptyV2={schemaVersion:2,assetCount:0,shards:[]},emptyV1={schemaVersion:1,assets:[]};
test('entry bounds actual decoded bytes including whitespace, with no Content-Length for v2 and v1',async()=>{
 assert.deepEqual(await fetchCatalogEntry({fetcher:async()=>new Response(JSON.stringify(emptyV2))}),emptyV2);
 for(const legacy of [false,true]){let count=0;await assert.rejects(()=>fetchCatalogEntry({fetcher:async()=>{count++;if(legacy&&count===1)return new Response('',{status:404});return new Response(JSON.stringify(legacy?emptyV1:emptyV2)+' '.repeat(262144));}}),/exceeds expected size/);assert.equal(count,legacy?2:1);}
 assert.deepEqual(await fetchCatalogEntry({fetcher:async path=>path==='./catalog-v2.json'?new Response('',{status:404}):new Response(JSON.stringify(emptyV1))}),emptyV1);
});
test('entry timeout covers stalled headers, stalled decoded body, and fallback; cancels body',async()=>{
 const keepAlive=setTimeout(()=>{},100);try{
 await assert.rejects(()=>fetchCatalogEntry({timeoutMs:5,fetcher:async(p,{signal})=>new Promise((resolve,reject)=>signal.addEventListener('abort',()=>reject(signal.reason),{once:true}))}),{name:'TimeoutError'});
 for(const legacy of [false,true]){let canceled=false;await assert.rejects(()=>fetchCatalogEntry({timeoutMs:5,fetcher:async p=>legacy&&p==='./catalog-v2.json'?new Response('',{status:404}):new Response(new ReadableStream({cancel(){canceled=true;}}))}),{name:'TimeoutError'});assert.equal(canceled,true);}
 }finally{clearTimeout(keepAlive);}
});
test('real gzip catalog entry checks decoded limit without compressed-length confusion',async()=>{
 let payload=JSON.stringify(emptyV2);const server=createServer((req,res)=>{const compressed=gzipSync(payload);res.writeHead(200,{'Content-Encoding':'gzip','Content-Length':compressed.length});res.end(compressed);});await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));try{const base=`http://127.0.0.1:${server.address().port}/`,fetcher=(path,options)=>fetch(new URL(path,base),options);assert.deepEqual(await fetchCatalogEntry({fetcher}),emptyV2);payload+=' '.repeat(262144);await assert.rejects(()=>fetchCatalogEntry({fetcher}),/exceeds expected size/);}finally{await new Promise(resolve=>server.close(resolve));}
});
