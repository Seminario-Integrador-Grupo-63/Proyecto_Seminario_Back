from datetime import datetime
from enum import StrEnum
from typing import Optional

from sqlmodel import SQLModel, Field, ForeignKey, create_engine

class OrderState(StrEnum):
    processing = "processing"
    waiting = "waiting"
    preparation = "preparation"
    cancelled = "cancelled"
    delivered = "delivered"
    closed = "closed"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str = Field(...)
    password: str = Field(...)
    email: str = Field(...)

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    last_name: str = Field(...)
    user: Optional[int] = Field(foreign_key="user.id") #Sacar el optional cuando este terminado la creacion d eusuario

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    restaurant: Optional[int] = Field(foreign_key="restaurant.id") #Sacar el optional cuando este terminado la creacion d eusuario

class Dish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    description: Optional[bytes] = None #A DEFINIR (LA DESCRIPCION E IMAGEN SON OBLITARIAS O NO?)
    image: Optional[bytes] = None
    preparation_time: Optional[int]
    category: int = Field(foreign_key="category.id")
    price: float = Field(...)

class SideDish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    description: Optional[bytes] = None 
    image: Optional[bytes] = None
    extra_price: float = Field(nullable=True, default=0.0)

class SideDishOptions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dish: int = Field(foreign_key="dish.id")
    side_dish: Optional[int] = Field(foreign_key="sidedish.id", nullable=True)

class Table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_booked: bool = Field(default=False)
    qr_id: str | None = "" #uuid4 for a unique qr code id
    restaurant: Optional[int] = Field(foreign_key="restaurant.id") #Sacar el optional cuando este terminado la creacion d eusuario

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    table: int = Field(foreign_key="table.id")
    total: float = Field(default=0.0)
    created_at: datetime = Field(...)
    state: OrderState = Field(default=OrderState.processing)

class OrderDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dish_selected: int = Field(foreign_key="sidedishoptions.id")
    order: Optional[int] = Field(foreign_key="order.id")
    sub_total: float = Field(...)
    customer: str = Field(...)
    observation: str = Field(default="")

class Waiter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
