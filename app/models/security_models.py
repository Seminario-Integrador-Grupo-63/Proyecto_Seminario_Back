
from pydantic import BaseModel, Field

from models import Restaurant, User


class RegistrationData(BaseModel):
    restorant_data: Restaurant = Field(...)
    user_data: User = Field(...)

class UserData(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
    