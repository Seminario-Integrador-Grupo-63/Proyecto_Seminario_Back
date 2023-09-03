
from fastapi import APIRouter
from models import Table
from services.db_service import db_service
from services.table_service import generate_qrcode, update_uuid

table_router = APIRouter(prefix="/table", tags=["Tables"])

@table_router.get("/", response_model=list[Table])
async def get_tables():
    return db_service.get_list_from_db(Table)

@table_router.get("/{id}")
async def get_table(id: int):
    return db_service.get_object_by_id(Table, id)

@table_router.post("/")
async def create_table(body: Table):
    return db_service.create_object(body)

@table_router.put("/")
async def update_table(body: Table):
    return db_service.update_object(Table, body)

@table_router.get("/{table_id}/qrcode")
async def get_qrcode(table_id: int):
    return await generate_qrcode(table_id)

@table_router.post("/{table_id}/qrcode")
async def update_qrcode(table_id:int, uuid_code: str):
    return await update_uuid(table_id=table_id, uuid_code=uuid_code)

