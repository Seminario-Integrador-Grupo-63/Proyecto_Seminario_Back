from fastapi import APIRouter, Response, status
from sqlmodel import select
from models import SideDishOptions
from services.db_service import db_service

sidedish_option_router = APIRouter(prefix="/side-dish-options", tags=["Side Dish options"])

@sidedish_option_router.get("/", response_model=list[SideDishOptions])
async def get_options():
    statement = select(SideDishOptions).where(SideDishOptions.is_active == True)
    value = db_service.get_with_filters(statement)
    return value

@sidedish_option_router.get("/{id}")
async def get_options(id: int):
    return db_service.get_object_by_id(SideDishOptions, id)

@sidedish_option_router.post("/")
async def create_options(body: SideDishOptions):
    return db_service.create_object(body)   

@sidedish_option_router.put("/")
async def update_options(body: SideDishOptions):
    return db_service.update_object(SideDishOptions, body)

@sidedish_option_router.delete("/{id}")
async def remove_sector(id:int):
    body: SideDishOptions = db_service.get_object_by_id(SideDishOptions,id)
    body.is_active = False
    db_service.update_object(SideDishOptions,body)
    return Response(status_code=status.HTTP_200_OK)