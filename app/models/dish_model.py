
from pydantic import BaseModel, Field

from models import Dish, SideDishOptions


class DishData(BaseModel):
    dish: Dish = Field(...)
    options: list[SideDishOptions] = Field(...)