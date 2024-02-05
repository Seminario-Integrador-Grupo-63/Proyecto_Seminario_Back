import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import select

from models import Restaurant, User, UserRolesEnum
from models.security_models import RegistrationData, UserData
from services.db_service import db_service

async def create_admin(registration_data: RegistrationData):
    try:
        user: User = registration_data.user_data
        restaurant_data: Restaurant = registration_data.restorant_data
        restaurant: Restaurant = db_service.create_object(restaurant_data)
        user.restaurant = restaurant.id
        db_service.create_object(user)
        
    except Exception as e:
        return e

async def create_employee(user: User):
    try:
        return db_service.create_object(user)
    except Exception as e:
        return e

async def create_user(user: User):
    if user.role == UserRolesEnum.admin:
        return await create_admin(user)
    elif user.role == UserRolesEnum.employee:
        return await create_employee(user)
    else:
        ...

async def login_user(user_data: UserData):
    statement = select(User).where(User.user == user_data.user, User.password == user_data.password)
    user = db_service.get_with_filters(statement)
    return user

async def get_employee_users(restaurant_id: str):
    statement = select(User).where(User.restaurant == restaurant_id, User.role == UserRolesEnum.employee)
    users: list[User] = db_service.get_with_filters(statement)
    return users