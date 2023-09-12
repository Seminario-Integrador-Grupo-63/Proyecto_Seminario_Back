import pickle
from datetime import datetime

from sqlmodel import select
from models import Order, OrderDetail, Table
from services.db_service import db_service
from services.redis_service import redis_service


async def save_order_detail_to_cache(table_code:str, order_detail: OrderDetail):

    detail_list = redis_service.save_list(table_code, order_detail.dict())
    customer_set = redis_service.save_set(f"{table_code}_costumer", order_detail.customer)
    return detail_list

async def get_order_details(table_code:str):
    return redis_service.get_data(table_code)

async def confirm_order(table_code: str):
    total_price = 0.0

    statement = select(Table).where(Table.qr_id == table_code)
    table: Table = db_service.get_with_filters(statement)[0]
    detail_list = redis_service.get_data(table_code)

    order = Order(table=table.id, created_at=datetime.now())
    order: Order = db_service.create_object(order) 

    for detail in detail_list:
        detail.pop("id")
        order_detail = OrderDetail(**detail)
        order_detail.order = order.id
        
        total_price += order_detail.sub_total

        db_service.create_object(order_detail)
    
    order.total = total_price
    redis_service.delete_data(table_code)
    return db_service.update_object(Order, order)