
from fastapi import APIRouter, Header

from models import User
from models.security_models import UserData, RegistrationData
from services.security_service import *

security_router = APIRouter(tags=["Security"], prefix="/security")

@security_router.post("/signup")
async def signup(registration_data: RegistrationData):
    return await create_user(registration_data)

@security_router.post("/login")
async def login(user: UserData):
    return await login_user(user)

@security_router.get("/emplyees")
async def get_users(restaurant_id: int = Header(...)):
    return await get_employee_users(restaurant_id)
