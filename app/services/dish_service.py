
from sqlmodel import select
from models import Dish, SideDishOptions
from models.dish_model import DishData, UpdatePriceAction, UpdatePriceData
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

async def update_all_dishes(update_data: UpdatePriceData):
    ...

async def get_new_price(update_data: UpdatePriceData, old_price: float):
    percentage = (old_price * update_data.percentage / 100)
    if update_data.action == UpdatePriceAction.increase:
        return old_price + percentage
    else:
        return old_price - percentage

async def update_category_dishes(update_data: UpdatePriceData):
    statement = select(Dish).where(Dish.category == update_data.category_id)
    dish_list: list[Dish] = db_service.get_with_filters(statement)
    for dish in dish_list:
        dish.price = await get_new_price(update_data, dish.price)
        db_service.update_object(Dish, dish)
        statement = select(SideDishOptions).where(SideDishOptions.dish == dish.id)
        sidedish_option_list: list[SideDishOptions] = db_service.get_with_filters(statement)
        for option in sidedish_option_list:
            option.extra_price = await get_new_price(update_data, option.extra_price)
            db_service.update_object(SideDishOptions, option)

async def update_dish_prices(update_data: UpdatePriceData):
    if update_data.category_id:
        return await update_category_dishes(update_data)
    else:
        ...