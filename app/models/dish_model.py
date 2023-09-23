
from enum import StrEnum
from pydantic import BaseModel, Field

from models import Category, Dish, SideDishOptions

class UpdatePriceAction(StrEnum):
    increase = "increase"
    decrease = "decrease"

class DishData(BaseModel):
    dish: Dish = Field(...)
    options: list[SideDishOptions] = Field(...)

class UpdatePriceData(BaseModel):
    percentage: float = Field(...)
    category_id: int | None = None
    action: UpdatePriceAction = Field(...)