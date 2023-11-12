from fastapi import APIRouter
from services.mock_service import create_mocks

mock_router = APIRouter(prefix="/mock", tags=["Mock"])

@mock_router.post("/")
async def create_mock():
    return create_mocks()