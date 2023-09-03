from fastapi import APIRouter
from models import Order, OrderDetail
from services.db_service import db_service
from services.order_service import confirm_order, get_order_details, save_order_detail_to_cache

order_router = APIRouter(prefix="/order", tags=["Orders"])

@order_router.get("/", response_model=list[Order])
async def get_orders():
    return db_service.get_list_from_db(Order)

@order_router.get("/{id}")
async def get_order(id: int):
    return db_service.get_object_by_id(Order, id)

@order_router.post("/{table_id}")
async def create_order(table_id: str):
    return await confirm_order(table_id)

@order_router.post("/detail/{table_code}")
async def add_order_detail(table_code:str, body: OrderDetail):
    return await save_order_detail_to_cache(table_code, body)

@order_router.get("/detail/{table_code}")
async def get_details(table_code:str):
    return await get_order_details(table_code)