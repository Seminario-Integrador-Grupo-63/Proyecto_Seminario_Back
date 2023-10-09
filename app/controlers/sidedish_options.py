from fastapi import APIRouter
from models import SideDishOptions
from services.db_service import db_service

sidedish_option_router = APIRouter(prefix="/side-dish-options", tags=["Side Dish options"])

@sidedish_option_router.get("/", response_model=list[SideDishOptions])
async def get_options():
    return db_service.get_list_from_db(SideDishOptions)

@sidedish_option_router.get("/{id}")
async def get_options(id: int):
    return db_service.get_object_by_id(SideDishOptions, id)

@sidedish_option_router.post("/")
async def create_options(body: SideDishOptions):
    return db_service.create_object(body)   

@sidedish_option_router.put("/")
async def update_options(body: SideDishOptions):
    return db_service.update_object(SideDishOptions, body)