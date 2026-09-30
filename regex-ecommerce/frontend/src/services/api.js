const BASE=import.meta.env.VITE_API_BASE_URL||'http://localhost:8000';
export async function api(path,options={}){const r=await fetch(`${BASE}${path}`,{...options,headers:{'Content-Type':'application/json',...(options.headers||{})}});if(!r.ok)throw new Error((await r.json().catch(()=>({detail:'Request failed'}))).detail||'Request failed');return r.status===204?null:r.json()}
