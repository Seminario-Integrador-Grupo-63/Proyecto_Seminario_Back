
from fastapi import APIRouter

from models import User
from models.security_models import *
from services.security_service import *

security_router = APIRouter(tags=["Security"])

@security_router.post("/signup")
async def signup(registration_data: RegistrationData):
    return await create_user(registration_data)