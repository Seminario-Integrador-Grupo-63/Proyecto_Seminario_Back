from fastapi import APIRouter, Header, Response, status
from models import Dish
from models.dish_model import UpdatePriceData
from services.db_service import db_service
from services.dish_service import *

dish_router = APIRouter(prefix="/dish", tags=["Dishes"])

@dish_router.get("/", response_model=list[Dish])
async def get_dishes(restaurant_id: int = Header(default=None), category_id: int = Header(default=None)):
    return await filter_dish(restaurant_id=restaurant_id, category_id=category_id)

@dish_router.get("/{dish_id}", response_model=DishData)
async def get_dish(dish_id: int):
    return await get_dish_data(dish_id)

@dish_router.post("/")
async def create_dish(dish_body: DishData):
    return await create_new_dish(dish_body)

@dish_router.put("/")
async def update_dish(dish_body: DishData):
    return await update_dish_data(dish_body)

@dish_router.post("/update_prices")
async def update_prices(body: UpdatePriceData, restaurant_id: int = Header(default=None)):
    return await update_dish_prices(update_data=body, restaurant_id=restaurant_id)

@dish_router.post("/update_prices/{uuid_code}")
async def confirm_prices(uuid_code: str):
    return await confirm_new_prices(uuid_code)

@dish_router.delete("/{id}")
async def remove_dish(id:int):
    body: Dish = db_service.get_object_by_id(Dish,id)
    body.is_active = False
    db_service.update_object(Dish,body)

    statements = select(SideDishOptions).where(SideDishOptions.dish==id)
    options: list[SideDishOptions] = db_service.get_with_filters(statements)
    for option in options:
        option.is_active = False
        db_service.update_object(SideDishOptions, option)
    return Response(status_code=status.HTTP_200_OK)