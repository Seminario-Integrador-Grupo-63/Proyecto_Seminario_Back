
import uuid
from sqlmodel import select
from models import Category, Dish, SideDish, SideDishOptions
from models.dish_model import DishData, DishPriceData, DishPricesDTO, MenuModel, OptionPriceData, SideDishData, UpdatePriceAction, UpdatePriceData, UpdatePrideCacheData
from services.db_service import db_service
from services.redis_service import redis_service


async def create_new_dish(dish: DishData):
    dish_data: Dish = dish.dish
    options_id: list[int] = dish.options
    dish = db_service.create_object(dish_data)
    for option_id in options_id:
        side_dish_option = SideDishOptions(dish=dish.id, sideDish=option_id)   
        db_service.create_object(side_dish_option) 
    side_dish_option = SideDishOptions(dish=dish.id)
    db_service.create_object(side_dish_option)

    return dish

async def update_dish_data(dish: DishData):
    dish_data: Dish = dish.dish
    options_id: list[int] = dish.options
    dish = db_service.update_object(Dish, dish_data)
    statement = select(SideDishOptions).where(SideDishOptions.dish==dish.id)
    side_dish_options: list[SideDishOptions] = db_service.get_with_filters(statement)
    for side_dish_option in side_dish_options:
        if side_dish_option.side_dish in options_id:
           options_id.remove(side_dish_option.side_dish)
        else:
            db_service.delete_row(SideDishOptions, [SideDishOptions.side_dish==side_dish_option.side_dish]) 
    for option_id in options_id:
        side_dish_option = SideDishOptions(dish=dish.id, sideDish=option_id)   
        db_service.create_object(side_dish_option) 

async def get_dish_data(dish_id: int):
    statement = select(SideDishOptions).where(SideDishOptions.dish == dish_id, SideDishOptions.is_active == True) 
    options: list[SideDishOptions] = db_service.get_with_filters(statement)
    dish = db_service.get_object_by_id(Dish, dish_id)
    side_dish_list = []
    for option in options:
        if option.side_dish:
            side_dish: SideDish = db_service.get_object_by_id(SideDish, option.side_dish)
            if side_dish.is_active:
                side_dish_data = SideDishData(side_dish_id= side_dish.id, 
                                            side_dish_name=side_dish.name,
                                            side_dish_description=side_dish.description,
                                            extra_price=option.extra_price)
                side_dish_list.append(side_dish_data)
    return DishData(dish=dish, options=side_dish_list)

async def update_all_dishes(update_data: UpdatePriceData):
    ...

async def get_new_price(update_data: UpdatePriceData, old_price: float):
    percentage = (old_price * update_data.percentage / 100)
    if update_data.action == UpdatePriceAction.increase:
        return old_price + percentage
    else:
        return old_price - percentage

"""async def update_category_dishes(update_data: UpdatePriceData):
    statement = select(Dish).where(Dish.category == update_data.category_id)
    dish_list: list[Dish] = db_service.get_with_filters(statement)
    for dish in dish_list:
        dish.price = await get_new_price(update_data, dish.price)
        db_service.update_object(Dish, dish)
        statement = select(SideDishOptions).where(SideDishOptions.dish == dish.id)
        sidedish_option_list: list[SideDishOptions] = db_service.get_with_filters(statement)
        for option in sidedish_option_list:
            option.extra_price = await get_new_price(update_data, option.extra_price)
            db_service.update_object(SideDishOptions, option)"""

async def cache_price_data(cache_data = list[UpdatePrideCacheData]):
    uuid_code = uuid_code = str(uuid.uuid4())
    for item in cache_data:
        redis_service.save_list(key=uuid_code, data=item, time=(3600))
    return uuid_code
    
async def filter_dish(restaurant_id: int | None = None, category_id: int | None = None):
    if restaurant_id:
        statement = select(Dish).where(Dish.restaurant == restaurant_id)
    elif category_id:
            statement = select(Dish).where(Dish.category == category_id)
    else:
        raise Exception("No id provided")
    statement = statement.where(Dish.is_active==True)
    return db_service.get_with_filters(statement)

async def get_new_prices(update_data: UpdatePriceData, dish_list: list[Dish]):
    dish_prices_list = []
    dish_prices_cache = []
    for dish in dish_list:
        dish_price = await get_new_price(update_data, dish.price)
        dish.price = dish_price
        statement = select(SideDishOptions).where(SideDishOptions.dish == dish.id)
        sidedish_option_list: list[SideDishOptions] = db_service.get_with_filters(statement)
        options_prices_list = []

        for option in sidedish_option_list:
            new_option_price = await get_new_price(update_data, option.extra_price)
            if option.side_dish:
                side_dish: SideDish = db_service.get_object_by_id(SideDish, option.side_dish)
                option.extra_price = new_option_price
                option_price_data = OptionPriceData(option_name=side_dish.name, option_price=option.extra_price)
                options_prices_list.append(option_price_data)

                dish_data = DishPriceData(dish_name=f"{dish.name} + {side_dish.name}",dish_price=dish.price, option_prices=options_prices_list)
                dish_prices_list.append(dish_data)

                cache_data = UpdatePrideCacheData(dish=dish, options=sidedish_option_list)
                dish_prices_cache.append(cache_data)
    
    uuid_code = await cache_price_data(dish_prices_cache)
    return DishPricesDTO(prices_code=uuid_code, dish_prices=dish_prices_list)
        


async def update_dish_prices(update_data: UpdatePriceData, restaurant_id: int):
    if update_data.category_id:
        dish_list = await filter_dish(category_id=update_data.category_id)
    else:
        dish_list = await filter_dish(restaurant_id=restaurant_id)
    
    return await get_new_prices(update_data, dish_list)


async def confirm_new_prices(uuid_code: str):
    cache_data: list[UpdatePrideCacheData] = redis_service.get_data(uuid_code)
    for item in cache_data:
        dish: Dish = item.dish
        option_list: list[SideDishOptions] = item.options
        db_service.update_object(model=Dish, body=dish)
        for option in option_list:
            db_service.update_object(model=SideDishOptions, body=option)
    redis_service.delete_data(uuid_code)

async def get_menu(restaurant_id: int):
    data = []
    statement = select(Category).where(Category.restaurant == restaurant_id, Category.is_active == True)
    categories: list[Category] =  db_service.get_with_filters(statement)
    for categorie in categories:
        statement = select(Dish).where(Dish.category == categorie.id, Dish.is_active == True)
        dishes = db_service.get_with_filters(statement)
        dish_data_list = []
        for dish in dishes:
            dish_data = await get_dish_data(dish.id)
            dish_data_list.append(dish_data)
        
        menu_data: MenuModel = MenuModel(category=categorie,
                                         dishes=dish_data_list)
        data.append(menu_data)
    return data