from fastapi import APIRouter, Header, Response, status
from sqlmodel import select
from models import SideDish, SideDishOptions
from services.db_service import db_service

sidedish_router = APIRouter(prefix="/side-dish", tags=["Side Dishes"])

@sidedish_router.get("/", response_model=list[SideDish])
async def get_sidedishes(restaurant_id: int = Header(...)):
    statement = select(SideDish).where(SideDish.restaurant == restaurant_id, SideDish.is_active==True)
    return db_service.get_with_filters(statement)

@sidedish_router.get("/{id}")
async def get_sidedish(id: int):
    return db_service.get_object_by_id(SideDish, id)

@sidedish_router.post("/")
async def create_sidedish(body: SideDish):
    return db_service.create_object(body)

@sidedish_router.put("/")
async def update_sidedish(body: SideDish):
    return db_service.update_object(SideDish, body)

@sidedish_router.delete("/{id}")
async def remove_sector(id:int):
    body: SideDish = db_service.get_object_by_id(SideDish,id)
    body.is_active = False
    db_service.update_object(SideDish,body)

    statements = select(SideDishOptions).where(SideDishOptions.side_dish==id)
    options: list[SideDishOptions] = db_service.get_with_filters(statements)
    for option in options:
        option.is_active = False
        db_service.update_object(SideDishOptions, option)
    return Response(status_code=status.HTTP_200_OK)