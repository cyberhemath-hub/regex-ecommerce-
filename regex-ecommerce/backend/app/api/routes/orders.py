from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,EmailStr,Field
from typing import List
from app.services.store import client
router=APIRouter(prefix='/api/orders',tags=['orders'])
class Customer(BaseModel):
    name:str=Field(min_length=2,max_length=120); email:str; phone:str=Field(min_length=10,max_length=20); address:str=Field(min_length=5,max_length=300); city:str; state:str; pin:str=Field(min_length=5,max_length=10)
class Item(BaseModel):
    product_id:str; size:str; quantity:int=Field(ge=1,le=10)
class OrderRequest(BaseModel):
    customer:Customer; items:List[Item]=Field(min_length=1,max_length=30)
@router.post('')
def create_order(payload:OrderRequest):
    # Order creation must be performed by a trusted DB transaction/RPC in production.
    # This endpoint intentionally does not accept client-submitted prices or mark payment paid.
    raise HTTPException(501,'Order transaction is not enabled yet. Configure and deploy the secure database order RPC before accepting live orders.')
