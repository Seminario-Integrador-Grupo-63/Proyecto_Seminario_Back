
from fastapi import APIRouter, Header, Response, status

from models import User
from models.security_models import UserData, RegistrationData
from services.security_service import *

security_router = APIRouter(tags=["Security"], prefix="/security")

@security_router.post("/signup")
async def signup(registration_data: User):
    return await create_user(registration_data)

@security_router.post("/login")
async def login(user: UserData):
    return await login_user(user)

@security_router.get("/employees")
async def get_users(restaurant_id: int = Header(...)):
    return await get_employee_users(restaurant_id)

@security_router.put("/employees")
async def update_user(body: User):
    if body.role == UserRolesEnum.employee:
        return db_service.update_object(User, body)
    else:
        return Response(content={"message": "You can only update employee users"}, status_code=status.HTTP_403_FORBIDDEN)

@security_router.delete("/employees/{user_id}")
async def delete_user(user_id: int):
    user: User = db_service.get_object_by_id(model=User, id=user_id)
    if user.role == UserRolesEnum.employee:
        return db_service.delete_row(User, [User.id==user_id])
    else:
        return Response(content={"message": "You can only delete employee users"}, status_code=status.HTTP_403_FORBIDDEN)

    