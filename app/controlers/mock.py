from fastapi import APIRouter
from services.mock_service import create_mocks
from services.mock_service_2_electric_bogaloo import create_mocks_2

mock_router = APIRouter(prefix="/mock", tags=["Mock"])

@mock_router.post("/")
async def create_mock():
    return create_mocks_2()