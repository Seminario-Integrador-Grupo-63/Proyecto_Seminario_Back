

from pydantic import BaseModel, Field

from models import Dish, Order, OrderDetail, OrderState, SideDish


class FullOrderData(BaseModel):
    order: Order
    order_details: list[OrderDetail] = Field(alias="orderDetail")

    class Config:
        allow_population_by_field_name = True

class OrderDetailData(BaseModel):
    ammount: int
    dish: Dish
    side_dish: SideDish | None = Field(alias="sideDish", default=None)
    sub_total: float = Field(alias="subTotal")
    observation: str

    class Config:
        allow_population_by_field_name = True

class CustomerOrderDetailData(BaseModel):
    customer: str
    order_detail: list[OrderDetailData] = Field(alias="orderDetails")
    customer_total: float | None = Field(default=None, alias="customerTotal")
    
    class Config:
        allow_population_by_field_name = True

class FullOrderDTO(BaseModel):
    id: int | None = None
    total_customers: int = Field(alias="totalCustomers")
    confirmed_customers: int = Field(alias="confirmedCustomera")
    order_details: list[CustomerOrderDetailData] = Field(alias="customerOrderDetail")
    date_created: str = Field(alias="CreatedAtDate")
    time_created: str = Field(alias="CreatedAtTime")
    total: float
    state: OrderState

    class Config:
        allow_population_by_field_name = True