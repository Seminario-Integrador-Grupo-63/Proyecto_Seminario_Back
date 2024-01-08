
from pydantic import BaseModel, Field

from models import Restaurant, User


class RegistrationData(BaseModel):
    restorant_data: Restaurant = Field(alias="restaurantData")
    user_data: User = Field(alias="userData")

    class Config:
        allow_population_by_field_name = True 

class UserData(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
    