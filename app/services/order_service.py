import pickle
from datetime import datetime

from sqlmodel import select
from models import Order, OrderDetail, OrderState, Table, TableState
from models.order_models import FullOrderData
from services import table_service
from services.db_service import db_service
from services.redis_service import redis_service


async def save_order_detail_to_cache(table_code:str, order_detail: OrderDetail):
    detail_list = redis_service.save_list(table_code, order_detail)
    customer_set, _ = redis_service.save_set(f"{table_code}_customer", order_detail.customer_name)
    return detail_list

async def remove_order_detail(table_code: str, order_detail: OrderDetail):
    order_detail_list: list[OrderDetail] = redis_service.remove_from_list(table_code, order_detail)
    has_order = False
    for detail in order_detail_list:
        if detail.customer_name == order_detail.customer_name:
            has_order = True
    if not has_order:
        redis_service.remove_from_list(f"{table_code}_customer", order_detail.customer_name)
    return order_detail_list

async def get_order_details(table_code:str):
    return redis_service.get_data(table_code)

async def confirm_order(table_code: str, customer_name:str):
    confirmed_costumers, _= redis_service.save_set(f"{table_code}_confirmed", customer_name)
    total_customers = redis_service.get_data(f"{table_code}_customer")

    if not len(confirmed_costumers) == len(total_customers):
        return {"confirmedCostumers": confirmed_costumers,
                "totalcostumers": total_customers}


    total_price = 0.0

    statement = select(Table).where(Table.qr_id == table_code)
    table: Table = db_service.get_with_filters(statement)[0]
    detail_list: list[OrderDetail] = redis_service.get_data(table_code)

    order = Order(table=table.id, created_at=datetime.now(), restaurant=table.restaurant, state=OrderState.waiting)
    order: Order = db_service.create_object(order) 

    for detail in detail_list:
        
        total_price += detail.sub_total
        detail.order = order.id
        db_service.create_object(detail)
    
    order.total = total_price
    updated_order = db_service.update_object(Order, order)

    await table_service.change_table_state(table_code, TableState.ocupied, TableState.waiting)

    redis_service.delete_data(table_code)
    redis_service.delete_data(f"{table_code}_confirmed")
    redis_service.delete_data(f"{table_code}_customer")

    
    return updated_order

async def get_full_order(order_id: int):
    order: Order = db_service.get_object_by_id(Order, order_id)

    statement = select(OrderDetail).where(OrderDetail.order == order_id)
    detail_list = db_service.get_with_filters(statement)

    return FullOrderData(order=order, order_details=detail_list)

async def confirm_preparation(order_id: int):
    order: Order = db_service.get_object_by_id(model=Order, id=order_id)
    order.state = OrderState.preparation
    new_order = db_service.update_object(model=Order, body=order)
    table: Table = db_service.get_object_by_id(model=Table, id=order.table)
    table.state = TableState.ocupied
    db_service.update_object(model=Table, body=table)
    return new_order
