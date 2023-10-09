
from enum import StrEnum
from pydantic import BaseModel, Field

from models import Category, Dish, SideDishOptions

class UpdatePriceAction(StrEnum):
    increase = "increase"
    decrease = "decrease"

class SideDishData(BaseModel):
    side_dish_id: int
    side_dish_name: str
    side_dish_description: str
    extra_price: str

class DishData(BaseModel):
    dish: Dish = Field(...)
    options: list[SideDishData] = Field(...)

class UpdatePriceData(BaseModel):
    percentage: float = Field(...)
    category_id: int | None = None
    action: UpdatePriceAction = Field(...)

class OptionPriceData(BaseModel):
    option_name: str
    option_price: str

class DishPriceData(BaseModel):
    dish_name: str
    dish_price: str
    option_prices: list[OptionPriceData] | None = None

class DishPricesDTO(BaseModel):
    prices_code: str
    dish_prices: list[DishPriceData]

class UpdatePrideCacheData(BaseModel):
    dish: Dish
    options: list[SideDishOptions]