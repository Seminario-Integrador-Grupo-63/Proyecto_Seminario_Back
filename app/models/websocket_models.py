
from enum import StrEnum
from pydantic import BaseModel, Field

class WebSocketActionEnum(StrEnum):
    confirm = "confirm"


class WebSocketData(BaseModel):
    action: WebSocketActionEnum = Field(...)
    table_code: str | None = ""
    customer: str | None = ""

class ConfirmationDTO(BaseModel):
    total_customers:int
    confirmed_customers: int
