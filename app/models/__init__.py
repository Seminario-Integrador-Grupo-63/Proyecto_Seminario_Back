from datetime import datetime
from enum import StrEnum
from typing import Optional
from pydantic import Extra

from sqlmodel import SQLModel, Field, ForeignKey, create_engine

class OrderState(StrEnum):
    processing = "processing" #Se escaneo el qr y se esta armando una orden
    waiting = "waiting" # Se confirmo la orden y se esta esperando la confirmacion del restaurante
    preparation = "preparation" # El restaurante confirmo la orden
    cancelled = "cancelled" # Cancelado
    delivered = "delivered" # Entregada en la mesa
    closed = "closed" # Pagada

class TableState(StrEnum):
    free = "free" # Desocupada
    ocupied = "ocupied" # Ocupada
    waiting = "waiting" # Esperando confirmacion de orden
    payment_ready = "payment_ready" # Cuenta pedida

class UserRolesEnum(StrEnum):
    admin = "admin"
    employee = "employee"

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    last_name: str = Field(alias="lastName")

    class Config:
        allow_population_by_field_name = True

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str = Field(unique=True)
    password: str = Field(...)
    email: str = Field(...)
    role: UserRolesEnum = Field(...)
    restaurant: int = Field(foreign_key="restaurant.id")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    image: Optional[str] = Field(default="")
    restaurant: int = Field(foreign_key="restaurant.id") 

class Dish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    description: Optional[bytes] = None #A DEFINIR (LA DESCRIPCION E IMAGEN SON OBLITARIAS O NO?)
    image: Optional[bytes] = None
    preparation_time: Optional[int] = Field(alias="preparationTime")
    category: int = Field(foreign_key="category.id")
    price: float = Field(...)
    restaurant: int = Field(foreign_key="restaurant.id") #Este no deberia ir pero es mas facil filrar asi
    
    class Config:
        allow_population_by_field_name = True

class SideDish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    description: Optional[bytes] = None 
    image: Optional[bytes] = None
    restaurant: int = Field(foreign_key="restaurant.id")

    class Config:
        extra = Extra.allow

class SideDishOptions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dish: int = Field(foreign_key="dish.id")
    side_dish: Optional[int] = Field(foreign_key="sidedish.id", nullable=True, alias="sideDish")
    extra_price: float = Field(nullable=True, default=0.0, alias="extraPrice")

    class Config:
        allow_population_by_field_name = True

class TableSector(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    restaurant: int = Field(foreign_key="restaurant.id")

class Table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    qr_id: str | None = Field(default="", alias="qrID") #uuid4 for a unique qr code id
    restaurant: int = Field(foreign_key="restaurant.id")
    sector: int = Field(foreign_key="tablesector.id")
    state: TableState | None = Field(default=TableState.free)
    
    class Config:
        allow_population_by_field_name = True

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    table: int = Field(foreign_key="table.id")
    total: float = Field(default=0.0)
    created_at: datetime = Field(alias="createdAt")
    state: OrderState = Field(default=OrderState.processing)
    restaurant: int = Field(foreign_key="restaurant.id")

    class Config:
        allow_population_by_field_name = True

class OrderDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dish: int = Field(foreign_key="dish.id")
    side_dish: int | None = Field(foreign_key="sidedish.id", alias="sideDish", nullable=True, default=None)
    order: Optional[int] = Field(foreign_key="order.id")
    sub_total: float = Field(alias="subTotal")
    customer_name: str = Field(alias="customerName")
    amount: int
    observation: str = Field(default="")

    class Config:
        allow_population_by_field_name = True
        
class Waiter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
