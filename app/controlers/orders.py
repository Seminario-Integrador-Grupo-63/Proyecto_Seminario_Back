from datetime import timedelta
from fastapi import APIRouter, Header
from models import Order, OrderDetail
from services.db_service import db_service
from services.order_service import *

order_router = APIRouter(prefix="/order", tags=["Orders"])

@order_router.get("/", response_model=list[Order])
async def get_orders(restaurant_id: int = Header(...)):
    time = datetime.now() - timedelta(days=1)
    statement = select(Order).where(Order.restaurant == restaurant_id, Order.created_at >= time)
    return db_service.get_with_filters(statement)

@order_router.get("/{id}")
async def get_order(id: int):
    return await get_full_order(order_id=id)

@order_router.post("/{table_code}")
async def order_confirmation(table_code: str, customer_name: str):
    return await confirm_order(table_code, customer_name)

@order_router.post("/detail/{table_code}")
async def add_order_detail(table_code:str, body: OrderDetail):
    return await save_order_detail_to_cache(table_code, body)

@order_router.get("/detail/{table_code}")
async def get_details(table_code:str):
    return await get_order_details(table_code)

@order_router.delete("/detail/{table_code}")
async def remove_detail(table_code: str, body: OrderDetail):
    return await remove_order_detail(table_code=table_code, order_detail=body)

@order_router.post("/preparation/{order_id}")
async def confirm_order_preparation(order_id: int):
    return await confirm_preparation(order_id)

@order_router.post("/deliverd/{order_id}")
async def change_state_to_delivered(order_id: int):
    return await deliver_order(order_id=order_id)

@order_router.post("cancelled/{order_id}")
async def order_cancelation(order_id: int):
    return await cancel_order(order_id)

@order_router.post("/creation/{table_code}", response_model=Order)
async def restaurant_order_creation(table_code: str, order_details: list[OrderDetail]):
    return await create_order_from_restaurant(table_code, order_details)