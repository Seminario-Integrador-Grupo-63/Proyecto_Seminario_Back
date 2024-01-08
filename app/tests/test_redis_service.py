import pytest

from services.redis_service import RedisService

def test_save_data():
    table_code = "1234567"
    customer = "c1"
    customer_2 = "c2"
    customer_list = [customer, customer_2]
    
    redis_service = RedisService()

    for item in customer_list:
        data, _ = redis_service.save_set(f"set_{table_code}", item)

        assert item in data

        data_2: list = redis_service.save_list(f"list_{table_code}", item)

        assert item in data_2
        