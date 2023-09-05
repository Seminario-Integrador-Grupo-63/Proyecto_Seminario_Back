from fastapi.testclient import TestClient
import pytest
from sqlmodel import select
from models import SideDishOptions
from services.db_service import db_service

from tests.factories import DishFactory

@pytest.mark.asyncio
async def test_dish_creation(test_client: TestClient):
    dish = DishFactory.build()

    response = test_client.post(url="/dish", data=dish.json())

    response.raise_for_status()
    dish_data = response.json()
    statement = select(SideDishOptions).where(SideDishOptions.dish == dish_data.get("id"))
    side_dish_option: SideDishOptions = db_service.get_with_filters(statement)

    assert isinstance(side_dish_option, SideDishOptions)
    assert side_dish_option.side_dish == None