
import pickle
from typing import Set
from fastapi import WebSocket, WebSocketDisconnect

from models.websocket_models import ConfirmationDTO, WebSocketData

from services.redis_service import redis_service


async def order_confirmation(data: WebSocketData, sockets: set[WebSocket]):
        
        customer_set = redis_service.get_data(f"{data.table_code}_customer") #pickle.loads(redis_client.get(f"{data.table_code}_customer"))
        confirmation_set, _ = redis_service.save_set(f"{data.table_code}_confirmed", data.customer) #pickle.loads(redis_client.get(f"{data.table_code}_confirmed")) if redis_client.get(f"{data.table_code}_confirmed") else set()
        
        confirmation_data = ConfirmationDTO(total_costumers=len(customer_set), confirmed_costumers=len(confirmation_set)).json()

        for socket in sockets:
             socket.send_json(confirmation_data)


async def websocket_conection(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            
            data = await websocket.receive_json()
            data = WebSocketData(**data)

            sockets: Set[WebSocket] = redis_service.save_set(f"{data.table_code}_sockets", websocket) #pickle.loads(redis_client.get(f"{data.table_code}_sockets")) if redis_client.get(f"{data.table_code}_sockets") else set()

            order_confirmation(data, sockets)
    
    except WebSocketDisconnect:
        ...