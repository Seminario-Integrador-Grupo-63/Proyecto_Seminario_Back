
from pydantic import BaseModel, Field

from models import Table, TableSector


class QRcodeData(BaseModel):
    table_id: int = Field(alias="tableId")
    uuid_code: str = Field(alias="uuidCode")
    qrcode: str = Field(alias="qrCode")

    class Config:
        allow_population_by_field_name = True
    
class TableGridList(BaseModel):
    sector: str | TableSector
    tables: list[Table] 

    class Config:
        allow_population_by_field_name = True