import pickle
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from models.websocket_models import WebSocketData
from services.websocket_service import websocket_conection

websocket_router = APIRouter(prefix="/ws", tags=["Websockets"])

@websocket_router.websocket("/confirmation")
async def websocket(websocket: WebSocket):
    await websocket_conection(websocket)