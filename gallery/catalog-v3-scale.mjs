// Generated local metadata only. No synthetic asset is published or counted as real.
import {readFile,writeFile} from 'node:fs/promises';import {performance} from 'node:perf_hooks';
import assert from 'node:assert/strict';
import {buildPagedCatalog,pinPagedCatalog,appendCatalog} from './catalog-v3.mjs';
import {createPagedCatalogStore,V3} from '../docs/core-catalog-v3.mjs';
import {SOURCE,assetSource,rawURL} from '../docs/core.mjs';
const base={schemaVersion:1,collection:{title:'SYNTHETIC SCALE QA ONLY'},source:{...SOURCE,commit:'1'.repeat(40)},sources:{},assets:[]},digest='a'.repeat(64);
const sizes=(process.env.SCALE_COUNTS||'10000,50000').split(',').map(Number),reports=[];
for(const count of sizes){
 const c=structuredClone(base);
 for(let i=0;i<count;i++){const id='scale-'+String(i).padStart(6,'0'),sourceId='source-'+i;c.sources[sourceId]={...SOURCE,commit:i.toString(16).padStart(40,'1')};c.assets.push({id,sourceId,title:`Synthetic coastal prop ${i} 海风`,description:`Original low-poly local test fixture with repeated structural words and exact serial ${i}; synthetic data, not a published asset. Large-scope query token group-${i%17}.`,version:'1.0.0',category:'category-'+i%20,assetKind:['prop','modular','scene'][i%3],theme:'theme-'+i%1000,style:['soft','blocky'][i%2],bounds:{x:1,y:1,z:1,unit:'m'},triangles:20,materials:1,status:'verified',license:'All rights reserved',files:Object.fromEntries([['glb','glb'],['blend','blend'],['generator','py'],['render','png'],['reference','png']].map(([role,ext])=>[role,{path:`assets/fixture/${id}/v1.0.0/${role}.${ext}`,size:10,sha256:digest}]))});}
 const start=performance.now(),built=buildPagedCatalog(c),buildMs=Math.round(performance.now()-start),root=pinPagedCatalog(built.template,'3'.repeat(40));let requests=0,bytes=0;
 const fetcher=async(url,options)=>{assert.equal(options.credentials,'omit');assert.equal(options.redirect,'error');const path=url.split('/'+'3'.repeat(40)+'/')[1],body=built.files.get(path);assert.ok(body);requests++;bytes+=body.length;return new Response(body);};
 const store=createPagedCatalogStore(root,{fetcher,entryBytes:Buffer.byteLength(JSON.stringify(root)+'\n')});const initial=await store.bootstrap(),first=initial.page;assert.deepEqual(first.assets.map(a=>a.id),c.assets.slice(0,24).map(a=>a.id));assert.equal(first.matchedTotal,count);
 assert.equal(initial.facetFailures.length,0);assert.ok(initial.metrics.bytes<=V3.queryBytes);assert.ok(initial.metrics.requests<=V3.queryRequests);
 const startup={rootBytes:Buffer.byteLength(JSON.stringify(root)+'\n'),graphBytes:bytes,requests:requests+1,firstPageRequests:first.metrics.requests,firstPageBytes:first.metrics.bytes};startup.totalBytes=startup.rootBytes+startup.graphBytes;
 assert.ok(startup.totalBytes<262144,'Startup is below one old single-file limit even at 50k');assert.ok(startup.requests<=16);
 const backRequests=requests;await store.query();assert.equal(requests,backRequests);
 const late=c.assets.at(-1);const lateResult=await store.query({query:late.id});assert.deepEqual(lateResult.assets.map(a=>a.id),[late.id]);assert.equal(lateResult.matchedTotal,1);
 const filter={theme:'theme-999',style:'blocky',assetKind:'scene'};let cursor=null,found=[],filterBytes=0,filterRequests=0;do{const page=await store.query(filter,{cursor});found.push(...page.assets);cursor=page.cursor;filterBytes+=page.metrics.bytes;filterRequests+=page.metrics.requests;}while(cursor);
 assert.deepEqual(found.map(a=>a.id),c.assets.filter(a=>a.theme===filter.theme&&a.style===filter.style&&a.assetKind===filter.assetKind).map(a=>a.id));
 const counts=store.stats();assert.ok(counts.cacheBytes<=V3.cacheBytes);assert.ok(counts.cacheNodes<=V3.cacheNodes);
 const report={synthetic:true,count,buildMs,...built.report,startup,lateSearch:lateResult.metrics,combinedFilter:{matches:found.length,bytes:filterBytes,requests:filterRequests},cache:counts};reports.push(report);console.log(JSON.stringify(report));
}
if(process.env.SCALE_REPORT)await writeFile(process.env.SCALE_REPORT,JSON.stringify(reports,null,2)+'\n');
