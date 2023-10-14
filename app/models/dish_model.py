
from enum import StrEnum
from pydantic import BaseModel, Field

from models import Category, Dish, SideDishOptions

class UpdatePriceAction(StrEnum):
    increase = "increase"
    decrease = "decrease"

class SideDishData(BaseModel):
    side_dish_id: int = Field(alias="sideDishID")
    side_dish_name: str = Field(alias="sideDishName")
    side_dish_description: str = Field(alias="sideDishDescription")
    extra_price: str = Field(alias="extraPrice")

    class Config:
        allow_population_by_field_name = True

class DishData(BaseModel):
    dish: Dish = Field(...)
    options: list[SideDishData] = Field(...)

class UpdatePriceData(BaseModel):
    percentage: float = Field(...)
    category_id: int | None = Field(default=None, alias="categoryId")
    action: UpdatePriceAction = Field(...)

    class Config:
        allow_population_by_field_name = True

class OptionPriceData(BaseModel):
    option_name: str
    option_price: str

class DishPriceData(BaseModel):
    dish_name: str = Field(alias="dishName")
    dish_price: str = Field(alias="dishPrice")
    option_prices: list[OptionPriceData] | None = Field(default=None, alias="optionPrices")

    class Config:
        allow_population_by_field_name = True

class DishPricesDTO(BaseModel):
    prices_code: str
    dish_prices: list[DishPriceData] = Field(alias="dishPrices")

    class Config:
        allow_population_by_field_name = True
        
class UpdatePrideCacheData(BaseModel):
    dish: Dish
    options: list[SideDishOptions]