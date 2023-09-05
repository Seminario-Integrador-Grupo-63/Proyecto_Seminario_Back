import pickle
from datetime import datetime

from sqlmodel import select
from models import Order, OrderDetail, Table
from services.db_service import db_service


async def save_order_detail_to_cache(table_code:str, order_detail: OrderDetail):
    from main import redis_client

    detail_list = pickle.loads(redis_client.get(table_code)) if redis_client.get(table_code) else []
    customer_set = pickle.loads(redis_client.get(f"{table_code}_customer")) if redis_client.get(f"{table_code}_customer") else set()
    detail_list.append(order_detail.dict())
    customer_set.add(order_detail.customer)
    redis_client.set(table_code, pickle.dumps(detail_list))
    redis_client.set(f"{table_code}_customers", pickle.dumps(customer_set))
    return detail_list

async def get_order_details(table_code:str):
    from main import redis_client
    
    return pickle.loads(redis_client.get(table_code)) if redis_client.get(table_code) else None

async def confirm_order(table_code: str):
    from main import redis_client

    total_price = 0.0

    statement = select(Table).where(Table.qr_id == table_code)
    table: Table = db_service.get_with_filters(statement)[0]
    detail_list = pickle.loads(redis_client.get(table_code))

    order = Order(table=table.id, created_at=datetime.now())
    order: Order = db_service.create_object(order) 

    for detail in detail_list:
        detail.pop("id")
        order_detail = OrderDetail(**detail)
        order_detail.order = order.id
        
        total_price += order_detail.sub_total

        db_service.create_object(order_detail)
    
    order.total = total_price
    redis_client.delete(table_code)
    return db_service.update_object(Order, order)