import {rawURL,filterAssets,formatBytes,validateCatalog,assetSource} from './core.mjs';
import {createCatalogStore} from './core-catalog-v2.mjs';
import {createPagedCatalogStore,fetchPagedCatalogEntry,FACETS} from './core-catalog-v3.mjs';
const $=s=>document.querySelector(s), statuses={prototype:'试产样品',review:'待审阅',verified:'已验证'};
let catalog, selected, selectedCatalog, mode='render', viewer, pendingLoad, sequence=0;
let pagedStore, browseReady=false, browseAbort, browseSequence=0, currentCursor=null, nextCursor=null, previousCursors=[], requestedCursor=null, requestedNavigation, queryTimer;
const facetCursors=new Map();
const node=(tag,text,className)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(className)e.className=className;return e;};
const readFilters=()=>Object.fromEntries(['query','repository','assetKind','category','theme','style'].map(k=>[k,$('#'+k).value]));
function draw(){const assets=filterAssets(catalog.assets,readFilters());renderCards(assets,`${assets.length} / ${catalog.assets.length} 件已入库`);}
function renderCards(assets,label){const pageCatalog=catalog;$('#catalog').replaceChildren();$('#count').textContent=label;
 for(const a of assets){const card=node('button',undefined,'card');card.type='button';const cover=node('div',undefined,'card-image'),img=node('img');img.src=rawURL(assetSource(catalog,a),a.files.render.path);img.loading='lazy';img.alt=a.title+' · 渲染图';img.addEventListener('error',()=>{cover.replaceChildren(node('span','预览图暂不可用'));},{once:true});cover.append(img);const body=node('div',undefined,'card-body');body.append(node('span',`${a.category} / ${a.theme}`,'eyebrow'),node('h3',a.title));const meta=node('div',undefined,'card-meta');meta.append(node('span',a.triangles.toLocaleString()+' triangles'),node('span',statuses[a.status]));body.append(meta);card.append(cover,body);card.addEventListener('click',()=>openAsset(a,pageCatalog));$('#catalog').append(card);}
 $('#empty').hidden=assets.length>0;if((pagedStore?.total||catalog.assets.length)){$('#empty h3').textContent='没有匹配的素材';$('#empty p').textContent='试试其他关键词，或重置筛选。';}
}
function release(){sequence++;pendingLoad?.abort();pendingLoad=null;viewer?.dispose();viewer=null;$('#viewer').replaceChildren();$('#reset-view').disabled=true;}
async function setMode(next){release();mode=next;const token=sequence;document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));$('#viewer-status').textContent='';$('#preview').hidden=next==='3d';$('#viewer').hidden=next!=='3d';
 if(next!=='3d'){const f=selected.files[next];if(!f){$('#preview').removeAttribute('src');$('#viewer-status').textContent='尚未提供参考图';return;}$('#preview').alt=selected.title+(next==='render'?' · 渲染图':' · 参考图');$('#preview').onerror=()=>{if(token===sequence&&mode===next)$('#viewer-status').textContent='图片暂不可用，请稍后重试。';};$('#preview').onload=()=>{if(token===sequence&&mode===next)$('#viewer-status').textContent='';};$('#preview').src=rawURL(assetSource(selectedCatalog,selected),f.path);return;}
 $('#viewer-status').textContent='正在按需载入 3D 预览…';try{const {createViewer}=await import('./viewer.mjs');if(token!==sequence)return;pendingLoad=new AbortController();const current=await createViewer($('#viewer'),rawURL(assetSource(selectedCatalog,selected),selected.files.glb.path),selected.files.glb,()=>token===sequence,pendingLoad.signal);if(token!==sequence){current?.dispose();return;}viewer=current;$('#viewer-status').textContent='';$('#reset-view').disabled=false;}catch(e){if(token===sequence){$('#viewer-status').textContent='3D 预览暂不可用，可查看渲染图或下载 GLB。';console.error(e);}}
}
function openAsset(a,pageCatalog=catalog){selected=a;selectedCatalog=pageCatalog;$('#detail-title').textContent=a.title;$('#detail-kind').textContent=[a.category,a.theme,a.style].join(' / ');$('#detail-description').textContent=a.description||'原创卡通场景素材。';$('#detail-status').textContent=statuses[a.status];$('#specs').replaceChildren();for(const [k,v] of [['版本',a.version],['类型',a.assetKind||'prop'],['三角面',a.triangles.toLocaleString()],['材质',a.materials],['尺寸（米）',`${a.bounds.x} × ${a.bounds.y} × ${a.bounds.z}`]])$('#specs').append(node('dt',k),node('dd',v));$('#downloads').replaceChildren();for(const [role,label] of [['glb','GLB 模型'],['blend','Blender 源文件'],['generator','生成脚本']]){const f=a.files[role],link=node('a');link.href=rawURL(assetSource(selectedCatalog,selected),f.path);link.target='_blank';link.rel='noopener noreferrer';link.append(node('span',label+' ↗'),node('span',formatBytes(f.size)));link.title=`SHA-256: ${f.sha256}`;$('#downloads').append(link);}$('#source-note').textContent='SOURCE / '+assetSource(selectedCatalog,a).repo+' @ '+assetSource(selectedCatalog,a).commit;document.querySelector('[data-mode="reference"]').disabled=!a.files.reference;$('#detail').showModal();setMode('render');}
$('#close').onclick=()=>$('#detail').close();$('#detail').addEventListener('close',()=>{release();selected=null;selectedCatalog=null;});$('#detail').addEventListener('click',e=>{if(e.target===$('#detail')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>setMode(b.dataset.mode));$('#reset-view').onclick=()=>viewer?.reset();$('#filters').addEventListener('submit',e=>e.preventDefault());$('#filters').addEventListener('input',()=>{if(!pagedStore){if(catalog)draw();return;}clearTimeout(queryTimer);browseAbort?.abort();queryTimer=setTimeout(()=>{previousCursors=[];browsePage(null);},180);});
$('#filters').addEventListener('reset',()=>{clearTimeout(queryTimer);browseAbort?.abort();setTimeout(()=>{previousCursors=[];if(pagedStore)browsePage(null);else if(catalog)draw();},0);});
function pageControls(busy=false){$('#previous-page').disabled=busy||previousCursors.length===0;$('#next-page').disabled=busy||!nextCursor;$('#catalog').setAttribute('aria-busy',String(busy));}
async function browsePage(cursor,{navigation,initialResult}={}){
 const token=++browseSequence;browseAbort?.abort();browseAbort=new AbortController();requestedCursor=cursor;requestedNavigation=navigation;$('#error').hidden=true;$('#retry-catalog').hidden=true;$('#catalog').replaceChildren();$('#empty').hidden=true;$('#count').textContent='正在查询全库目录…';pageControls(true);
 try{const result=initialResult||await pagedStore.query(readFilters(),{cursor,signal:browseAbort.signal});if(token!==browseSequence)return false;
  if(navigation==='next')previousCursors.push(currentCursor);if(navigation==='previous')previousCursors.pop();
  currentCursor=cursor;nextCursor=result.cursor;catalog=result;browseReady=true;
  const first=(cursor?.matched||0)+1,last=(cursor?.matched||0)+result.assets.length;
  const range=result.assets.length?`本页 ${first}–${last} 件`:'本页暂无匹配';
  const total=result.matchedTotal===null?'匹配总数尚未遍历完':`共 ${result.matchedTotal} 件匹配`;
  renderCards(result.assets,`${range} · ${total} · 全库 ${result.total} 件`);
  $('#page-status').textContent=result.budgetLimited?'本轮查询已达预算，可继续查找。':`第 ${previousCursors.length+1} 页，每页最多 24 件`;
  $('#next-page').textContent=result.budgetLimited?'继续查找':'下一页';
  if(!result.assets.length&&result.cursor){$('#empty h3').textContent='本轮尚未找到匹配';$('#empty p').textContent='查询尚未结束，请选择“继续查找”。';}
  pageControls();return true;
 }catch(error){if(token!==browseSequence||error.name==='AbortError')return false;$('#count').textContent='目录查询失败';$('#error').hidden=false;$('#error').textContent='本页未加载。检查网络后重试，已选筛选条件会保留。';$('#retry-catalog').hidden=false;pageControls(true);console.error(error);return false;}
}
function installFacet(field,page){const button=$('#'+field+'-more');for(const item of page.values)$('#'+field).append(new Option(`${item.value} (${item.count})`,item.value));facetCursors.set(field,page.cursor);button.hidden=!page.cursor;button.textContent='更多选项';}
async function loadFacet(field){
 const button=$('#'+field+'-more');button.disabled=true;
 try{const page=await pagedStore.facets(field,{after:facetCursors.get(field)||null});installFacet(field,page);}
 catch(error){button.hidden=false;button.textContent='重试选项';console.error(error);}finally{button.disabled=false;}
}
$('#previous-page').onclick=()=>browsePage(previousCursors.at(-1),{navigation:'previous'});
$('#next-page').onclick=()=>browsePage(nextCursor,{navigation:'next'});
$('#retry-catalog').onclick=()=>pagedStore&&browseReady?browsePage(requestedCursor,{navigation:requestedNavigation}):initialize();
for(const field of FACETS)$('#'+field+'-more').onclick=()=>loadFacet(field);
async function initialize(){
 try{const input=await fetchPagedCatalogEntry();if(input.schemaVersion===3){pagedStore=createPagedCatalogStore(input);browseReady=false;for(const field of FACETS){const button=$('#'+field+'-more');button.hidden=false;button.textContent='载入选项';}$('#pagination').hidden=false;const token=++browseSequence;browseAbort?.abort();browseAbort=new AbortController();const initial=await pagedStore.bootstrap(readFilters(),{signal:browseAbort.signal});if(token!==browseSequence)return;await browsePage(null,{initialResult:initial.page});for(const field of FACETS){if(initial.facets[field])installFacet(field,initial.facets[field]);else{const button=$('#'+field+'-more');button.hidden=false;button.textContent='载入选项';}}return;}
  $('#compatibility-note').hidden=false;
  if(input.schemaVersion===2){$('#count').textContent='正在校验兼容目录…';catalog=await createCatalogStore(input).load();}else catalog=validateCatalog(input);
  for(const a of catalog.assets)a._repository=assetSource(catalog,a).repo;
  for(const repo of [...new Set(catalog.assets.map(a=>a._repository))].sort())$('#repository').append(new Option(repo,repo));
  for(const key of ['assetKind','category','theme','style'])for(const v of [...new Set(catalog.assets.map(a=>a[key]))].sort())$('#'+key).append(new Option(v,v));draw();
 }catch(error){if(error.name==='AbortError')return;$('#count').textContent='目录读取失败';$('#error').hidden=false;$('#error').textContent='无法读取素材目录，请检查网络后重试。';$('#retry-catalog').hidden=false;console.error(error);}
}
await initialize();
