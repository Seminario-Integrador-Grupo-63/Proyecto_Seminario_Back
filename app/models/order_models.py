

from pydantic import BaseModel

from models import Order, OrderDetail


class FullOrderData(BaseModel):
    order: Order
    order_details: list[OrderDetail]