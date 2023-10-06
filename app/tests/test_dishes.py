from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
import pytest
from sqlmodel import select
from models import Category, Restaurant, SideDishOptions
from models.dish_model import DishPricesDTO, UpdatePriceData
from services.db_service import db_service
from services.redis_service import redis_service

from tests.factories import DishFactory

@pytest.mark.asyncio
async def test_dish_creation(test_client: TestClient):
    restaurant = db_service.get_list_from_db(Restaurant)[0]
    statement = select(Category).where(Category.restaurant == restaurant.id)
    category = db_service.get_with_filters(statement)[0]
    dish = DishFactory.build(restaurant=restaurant.id, category=category.id)

    response = test_client.post(url="/dish", data=dish.json())

    response.raise_for_status()
    dish_data = response.json()
    statement = select(SideDishOptions).where(SideDishOptions.dish == dish_data.get("id"))
    side_dish_option: SideDishOptions = db_service.get_with_filters(statement)[0]

    assert isinstance(side_dish_option, SideDishOptions)
    assert side_dish_option.side_dish == None

@pytest.mark.asyncio
async def test_total_prices_update(test_client: TestClient):
    price_data = UpdatePriceData(percentage=10.0, action="increase")
    headers = {"restaurant-id": "1"}
    response = test_client.post(url="/dish/update_prices", json=jsonable_encoder(price_data.dict()), headers=headers)
    response.raise_for_status()
    
    response_data: DishPricesDTO = DishPricesDTO(**response.json())
    cache_data = redis_service.get_data(response_data.prices_code)
    
    response_2 = test_client.post(url=f"/dish/update_prices/{response_data.prices_code}")