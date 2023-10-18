from fastapi import APIRouter, Header
from models import Order, OrderDetail
from services.db_service import db_service
from services.order_service import *

order_router = APIRouter(prefix="/order", tags=["Orders"])

@order_router.get("/", response_model=list[Order])
async def get_orders(restaurant_id: int = Header(...)):
    statement = select(Order).where(Order.restaurant == restaurant_id)
    return db_service.get_with_filters(statement)

@order_router.get("/{id}")
async def get_order(id: int):
    return get_full_order(order_id=id)

@order_router.post("/{table_id}")
async def create_order(table_id: str, customer_name: str):
    return await confirm_order(table_id, customer_name)

@order_router.post("/detail/{table_code}")
async def add_order_detail(table_code:str, body: OrderDetail):
    return await save_order_detail_to_cache(table_code, body)

@order_router.get("/detail/{table_code}")
async def get_details(table_code:str):
    return await get_order_details(table_code)

@order_router.delete("/detail/{tablr_code}")
async def remove_detail(table_dode: str, body: OrderDetail):
    return await remove_order_detail(table_code=table_dode, order_detail=body)