import io
from fastapi import FastAPI, Response
import qrcode
from fastapi.middleware.cors import CORSMiddleware
import base64

from services.db_service import db_service
from controlers import categories, dishes, sidedishes, tables, sidedish_options, orders, mock

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.category_router)
app.include_router(dishes.dish_router)
app.include_router(sidedishes.sidedish_router)
app.include_router(tables.table_router)
app.include_router(sidedish_options.sidedish_option_router)
app.include_router(orders.order_router)
app.include_router(mock.mock_router)

#db_service.create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}