from fastapi import APIRouter
from services.mock_service import create_mocks_in_db

mock_router = APIRouter(prefix="/mock", tags=["Mock"])

@mock_router.post("/")
async def create_mocks():
    return create_mocks_in_db()