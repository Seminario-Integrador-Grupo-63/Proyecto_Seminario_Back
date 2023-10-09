import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select

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

async def create_employee(registration_data: RegistrationData):
    try:
        user: User = registration_data.user_data
        restaurant_data: Restaurant = registration_data.restorant_data
        user.restaurant = restaurant_data.id
        db_service.create_object(user)
    except Exception as e:
        return e

async def create_user(registration_data: RegistrationData):
    user: User = registration_data.user_data
    if user.role == UserRolesEnum.admin:
        return await create_admin(registration_data)
    elif User.role == UserRolesEnum.employee:
        return await create_employee(registration_data)
    else:
        ...

async def login_user(user_data: UserData):
    statement = select(User).where(User.user == user_data.user, User.password == user_data.password)
    user = db_service.get_with_filters(statement)
    return user[0]