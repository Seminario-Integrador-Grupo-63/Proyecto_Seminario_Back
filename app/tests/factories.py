
from pydantic_factories import ModelFactory

from models import Dish


class DishFactory(ModelFactory):
    __model__ = Dish