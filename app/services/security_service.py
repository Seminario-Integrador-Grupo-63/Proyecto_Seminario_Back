import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select

from models import Restaurant, User, UserRolesEnum
from models.security_models import RegistrationData
from services.db_service import db_service

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', "abc")   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY', "123")    # should be kept secret

async def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


async def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

async def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

async def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

async def create_admin(registration_data: RegistrationData):
    try:
        user: User = registration_data.user_data
        restaurant_data: Restaurant = registration_data.restorant_data
        restaurant: Restaurant = db_service.create_object(restaurant_data)
        user.restaurant = restaurant.id
        user.password = get_hashed_password(user.password)
        db_service.create_object(user)
        
    except Exception as e:
        return e

async def create_employee(registration_data: RegistrationData):
    ...

async def create_user(registration_data: RegistrationData):
    user: User = registration_data.user_data
    if user.role == UserRolesEnum.admin:
        return await create_admin(registration_data)
    elif User.role == UserRolesEnum.employee:
        return await create_employee(registration_data)
    else:
        ...
    