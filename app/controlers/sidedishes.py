from fastapi import APIRouter
from models import SideDish
from services.db_service import db_service

sidedish_router = APIRouter(prefix="/side-dish", tags=["Side Dishes"])

@sidedish_router.get("/", response_model=list[SideDish])
async def get_sidedishes():
    return db_service.get_list_from_db(SideDish)

@sidedish_router.get("/{id}")
async def get_sidedish(id: int):
    return db_service.get_object_by_id(SideDish, id)

@sidedish_router.post("/")
async def create_sidedish(body: SideDish):
    return db_service.create_object(body)

@sidedish_router.put("/")
async def update_sidedish(body: SideDish):
    return db_service.update_object(SideDish, body)