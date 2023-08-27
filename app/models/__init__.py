from enum import StrEnum
from typing import Optional

from sqlmodel import SQLModel, Field, ForeignKey, create_engine

class OrderState(StrEnum):
    processing = "processing"
    waiting = "waiting"
    preparation = "preparation"
    cancelled = "cancelled"
    delivered = "delivered"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str = Field(...)
    password: str = Field(...)
    email: str = Field(...)

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    last_name: str = Field(...)
    user: Optional[int] = Field(foreign_key="user.id")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    restaurant: Optional[int] = Field(foreign_key="restaurant.id")

class Dish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    description: Optional[bytes] = None #A DEFINIR (LA DESCRIPCION E IMAGEN SON OBLITARIAS O NO?)
    image: Optional[bytes] = None
    preparation_time: Optional[int]
    category: Optional[int] = Field(foreign_key="category.id")
    price: float = Field(...)

class SideDish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    description: Optional[bytes] = None 
    image: Optional[bytes] = None
    extra_price: float = Field(nullable=True, default=0.0)

class SideDishOptions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dish: Optional[int] = Field(foreign_key="dish.id")
    side_dish: Optional[int] = Field(foreign_key="sidedish.id")

class Table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_booked: bool = Field(default=False)
    qr_id: str = Field(...) #uuid4 for a unique qr code id

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    table: Optional[int] = Field(foreign_key="table.id")
    total: float = Field(default=0.0)
    created_at: str # ADD EXTRA PYDANTIC TYPES FOR DATETIME
    state: OrderState = Field(default=OrderState.processing)

class OrderDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dish: Optional[int] = Field(foreign_key="dish.id")
    SideDish: Optional[int] = Field(foreign_key="sidedish.id")
    order: Optional[int] = Field(foreign_key="order.id")
    sub_total: float = Field(...)

#create db and engine
db_url = "postgresql://admin:admin@postgres:5432/root"

engine = create_engine(db_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

