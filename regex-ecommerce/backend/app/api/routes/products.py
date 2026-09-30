from fastapi import APIRouter,HTTPException
from app.services.store import client
router=APIRouter(prefix='/api/products',tags=['products'])
@router.get('')
def list_products():
    try:
        r=client().table('products').select('id,name,slug,description,price,compare_at_price,category_id,featured,bestseller,active,product_images(url,alt_text),product_variants(size,color,stock)').eq('active',True).order('created_at',desc=True).execute()
        out=[]
        for p in r.data:
            images=p.pop('product_images',[]) or []; variants=p.pop('product_variants',[]) or []
            out.append({'id':str(p['id']),'name':p['name'],'category':str(p.get('category_id') or 'Clothing'),'price':float(p['price']),'oldPrice':float(p['compare_at_price']) if p.get('compare_at_price') else None,'description':p.get('description') or '', 'image':images[0]['url'] if images else '', 'sizes':[v['size'] for v in variants if v.get('size')], 'stock':sum(v.get('stock',0) for v in variants),'badge':'BESTSELLER' if p.get('bestseller') else ('FEATURED' if p.get('featured') else 'REGEX')})
        return out
    except Exception as e: raise HTTPException(503,'Product catalogue unavailable. Check Supabase setup.') from e
@router.get('/{product_id}')
def get_product(product_id:str):
    data=list_products()
    p=next((x for x in data if x['id']==product_id),None)
    if not p: raise HTTPException(404,'Product not found')
    return p
