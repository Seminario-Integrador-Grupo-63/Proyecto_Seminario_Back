
from fastapi import APIRouter, Header
from sqlmodel import select
from models import Category
from services.db_service import db_service

category_router = APIRouter(prefix="/category", tags=["Categories"])

@category_router.get("/", response_model=list[Category])
async def get_categories(restaurant_id: int = Header(...)):
    statement = select(Category).where(Category.restaurant == restaurant_id)
    return db_service.get_with_filters(statement)

@category_router.get("/{category_id}")
async def get_category(category_id: int):
    return db_service.get_object_by_id(Category, category_id)

@category_router.post("/")
async def create_category(category_body: Category):
    return db_service.create_object(category_body)

@category_router.put("/")
async def update_category(category_body: Category):
    return db_service.update_object(Category, category_body)
