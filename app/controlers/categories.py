
from fastapi import APIRouter, Header, Response, status
from sqlmodel import select
from models import Category
from models.dish_model import MenuModel
from services.db_service import db_service
from services.dish_service import get_menu

category_router = APIRouter(prefix="/category", tags=["Categories"])

@category_router.get("/menu", response_model=list[MenuModel])
async def get_all_data(restaurant_id: int = Header(...)):
    return await get_menu(restaurant_id = restaurant_id)

@category_router.get("/", response_model=list[Category])
async def get_categories(restaurant_id: int = Header(...)):
    statement = select(Category).where(Category.restaurant == restaurant_id, Category.is_active == True)
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

@category_router.delete("/{id}")
async def remove_category(id:int):
    body: Category = db_service.get_object_by_id(Category,id)
    body.is_active = False
    db_service.update_object(Category,body)
    return Response(status_code=status.HTTP_200_OK)

