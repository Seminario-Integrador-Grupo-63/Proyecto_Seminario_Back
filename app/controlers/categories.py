
from fastapi import APIRouter
from models import Category
from services.db_service import db_service

category_router = APIRouter(prefix="/category", tags=["Categories"])

@category_router.get("/", response_model=list[Category])
async def get_categories():
    return db_service.get_list_from_db(Category)

@category_router.get("/{category_id}")
async def get_category(category_id: int):
    return db_service.get_object_by_id(Category, category_id)

@category_router.post("/")
async def create_category(category_body: Category):
    return db_service.create_object(category_body)

@category_router.put("/")
async def update_category(category_body: Category):
    return db_service.update_object(Category, category_body)
