export const SOURCE = Object.freeze({owner:'shAdow-XJY-Games',repo:'Shadow3DAssetLibrary'});
export const ALLOWED_REPOSITORIES = Object.freeze(['shAdow-XJY-Games/Shadow3DAssetLibrary']);
export function assetSource(catalog,asset){const source=asset.sourceId?catalog.sources?.[asset.sourceId]:catalog.source;if(!source)throw Error('Unknown source ID');return source;}
export function rawURL(source,path){
 if(!ALLOWED_REPOSITORIES.includes(`${source.owner}/${source.repo}`)||! /^[a-f0-9]{40}$/.test(source.commit)) throw Error('Unpinned asset source');
 if(!/^assets\/(?:(?:[A-Za-z0-9_-]+|v?[0-9]+[.][0-9]+[.][0-9]+)\/)*[A-Za-z0-9_-]+[.][A-Za-z0-9]+$/.test(path)||path.split('/').some(p=>!p||p==='.'||p==='..')) throw Error('Unsafe asset path');
 return `https://raw.githubusercontent.com/${source.owner}/${source.repo}/${source.commit}/${path.split('/').map(encodeURIComponent).join('/')}`;
}
export function filterAssets(assets,{query='',category='',theme='',style='',assetKind='',repository=''}={}){
 const q=query.trim().toLocaleLowerCase();return assets.filter(a=>(!repository||a._repository===repository)&&(!assetKind||a.assetKind===assetKind)&&(!category||a.category===category)&&(!theme||a.theme===theme)&&(!style||a.style===style)&&(!q||[a.id,a.title,a.description,a.category,a.theme,a.style].join(' ').toLocaleLowerCase().includes(q)));
}
export const formatBytes=n=>n<1024?`${n} B`:n<1048576?`${(n/1024).toFixed(1)} KB`:`${(n/1048576).toFixed(1)} MB`;
export function validateCatalog(c){
 if(c.schemaVersion!==1||!Array.isArray(c.assets))throw Error('Invalid catalog');
 if(c.source && !ALLOWED_REPOSITORIES.includes(`${c.source.owner}/${c.source.repo}`))throw Error('Unapproved default repository');
 for(const [id,source] of Object.entries(c.sources||{})){if(!/^[a-z0-9-]+$/.test(id))throw Error('Invalid source ID');rawURL(source,'assets/source-check.glb');}
 const ids=new Set();for(const a of c.assets){if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(a.id)||ids.has(a.id))throw Error('Invalid or duplicate ID');ids.add(a.id);
 if(!['prototype','review','verified'].includes(a.status)||a.license!=='All rights reserved')throw Error('Invalid status or license');
 for(const role of ['glb','blend','generator','render'])if(!a.files?.[role])throw Error('Missing file');
 for(const f of Object.values(a.files)){rawURL(assetSource(c,a),f.path);if(!Number.isInteger(f.size)||f.size<1||f.size>26214400||!/^[a-f0-9]{64}$/.test(f.sha256))throw Error('Invalid file record');}
 }return c;
}
