

from pydantic import BaseModel, Field

from models import Dish, Order, OrderDetail, OrderState, SideDish

class SideDishWithPrice(SideDish, table=False):
    price: float | None = Field(default=0.0, alias="extraPrice")

class FullOrderData(BaseModel):
    order: Order
    order_details: list[OrderDetail] = Field(alias="orderDetail")

    class Config:
        allow_population_by_field_name = True

class OrderDetailData(BaseModel):
    amount: int
    dish: Dish
    side_dish: SideDishWithPrice | None = Field(alias="sideDish", default=None)
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

class CustomerList(BaseModel):
    customer: str
    confirmed: bool

class FullOrderDTO(BaseModel):
    id: int | None = None
    total_customers: int = Field(alias="totalCustomers")
    confirmed_customers: int = Field(alias="confirmedCustomers")
    order_details: list[CustomerOrderDetailData] = Field(alias="customerOrderDetails")
    date_created: str | None = Field(alias="createdAtDate", default=None)
    time_created: str | None = Field(alias="createdAtTime", default=None)
    total: float
    state: OrderState
    customer_list: list[CustomerList] | None = Field(alias="customerList", default=[])

    class Config:
        allow_population_by_field_name = True
