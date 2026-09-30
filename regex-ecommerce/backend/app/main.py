from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import FRONTEND_URL
from app.api.routes import products,orders
app=FastAPI(title='REGEX Store API',version='1.0.0',description='Backend API for REGEX clothing store')
app.add_middleware(CORSMiddleware,allow_origins=[FRONTEND_URL,'http://localhost:5173'],allow_credentials=True,allow_methods=['GET','POST','PATCH','DELETE'],allow_headers=['Authorization','Content-Type'])
app.include_router(products.router);app.include_router(orders.router)
@app.get('/health')
def health(): return {'status':'ok','service':'regex-api'}
