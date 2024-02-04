
from fastapi import APIRouter, Header, Response, status
from models import Table, TableSector
from services.db_service import db_service
from services.table_service import *

table_router = APIRouter(prefix="/table", tags=["Tables"])
@table_router.get("/grid", response_model=list[TableGridList])
async def get_grids_tables(restaurant_id: int = Header(...)):
    return await get_tables_grid(restaurant_id=restaurant_id)

@table_router.get("/sector", response_model=list[TableSector])
async def get_sectors(restaurant_id: int = Header(...)):
    statement = select(TableSector).where(TableSector.restaurant == restaurant_id)
    return db_service.get_with_filters(statement)

@table_router.post("/sector")
async def create_table(body: TableSector):
    return db_service.create_object(body)

@table_router.put("/sector")
async def update_table(body: TableSector):
    return db_service.update_object(TableSector, body)

@table_router.delete("/sector/{id}")
async def remove_sector(id:int):
    body: TableSector = db_service.get_object_by_id(TableSector,id)
    body.is_active = False
    db_service.update_object(TableSector,body)

    statements = select(Table).where(Table.sector==id)
    tables: list[Table] = db_service.get_with_filters(statements)
    for table in tables:
        table.is_active = False
        db_service.update_object(SideDishOptions, table)
    return Response(status_code=status.HTTP_200_OK)

@table_router.get("/", response_model=list[Table])
async def get_tables(restaurant_id: int = Header(...)):
    statement = select(Table).where(Table.restaurant == restaurant_id)
    return db_service.get_with_filters(statement)

@table_router.get("/{id}")
async def get_table(id: int):
    return db_service.get_object_by_id(Table, id)

@table_router.post("/")
async def create_table(body: Table):
    return db_service.create_object(body)

@table_router.put("/")
async def update_table(body: Table):
    return db_service.update_object(Table, body)

@table_router.delete("/{id}")
async def remove_table(id:int):
    body: Table = db_service.get_object_by_id(Table,id)
    body.is_active = False
    db_service.update_object(Table,body)
    return Response(status_code=status.HTTP_200_OK)

@table_router.get("/{table_id}/qrcode", response_model=QRcodeData)
async def get_qrcode(table_id: int):
    return await generate_qrcode(table_id)

@table_router.post("/{table_id}/qrcode", response_model=Table)
async def update_qrcode(table_id:int, uuid_code: str):
    return await update_uuid(table_id=table_id, uuid_code=uuid_code)

@table_router.get("/{table_code}/orders", response_model=list[FullOrderDTO])
async def get_table_orders(table_code:str):
    return await get_current_orders(table_code=table_code)

@table_router.get("/{table_code}/bill", response_model=list[CustomerOrderDetailData])
async def get_table_billing(table_code: str):
    return await generate_billing(table_code)

@table_router.post("/{table_code}/bill")
async def billing_confirmation(table_code: str):
    return await close_table(table_code=table_code)

@table_router.post("/{table_code}/init")
async def init_tables(customer_name:str, table_code:str):
    return await init_table(table_code=table_code, customer_name=customer_name)

@table_router.post("/{table_code}/cancell")
async def table_cancelation(table_code: str):
    return await cancell_table(table_code=table_code)


