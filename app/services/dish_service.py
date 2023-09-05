
from sqlmodel import select
from models import Dish, SideDishOptions
from models.dish_model import DishData
from services.db_service import db_service


async def create_new_dish(dish: Dish):
    dish = db_service.create_object(dish)
    side_dish_option = SideDishOptions(dish=dish.id)
    db_service.create_object(side_dish_option)
    return dish

async def get_dish_data(dish_id: int):
    statement = select(SideDishOptions).where(SideDishOptions.dish == dish_id) 
    options = db_service.get_with_filters(statement)
    dish = db_service.get_object_by_id(Dish, dish_id)
    return DishData(dish=dish, options=options)