
from pydantic import BaseModel, Field


class QRcodeData(BaseModel):
    table_id: int = Field(...)
    uuid_code: str = Field(...)
    qrcode: str = Field(...)