from fastapi import APIRouter
from models import Dish
from services.db_service import db_service
from services.dish_service import create_new_dish, get_dish_data

dish_router = APIRouter(prefix="/dish", tags=["Dishes"])

@dish_router.get("/", response_model=list[Dish])
async def get_dishes():
    return db_service.get_list_from_db(Dish)

@dish_router.get("/{dish_id}")
async def get_dish(dish_id: int):
    return await get_dish_data(dish_id)

@dish_router.post("/")
async def create_dish(dish_body: Dish):
    return await create_new_dish(dish_body)

@dish_router.put("/")
async def update_dish(dish_body: Dish):
    return db_service.update_object(Dish, dish_body)