"""Class."""
from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self):
        """
        Crea una Lista de WebSocket
        """
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Agrega a la lista los usuarios conectados 
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        print(self.active_connections)
        print(type(websocket))
        print(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Elimina a la lista los usuarios conectados 
        """
        self.active_connections.remove(websocket)
        print(self.active_connections)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        print(self.active_connections[websocket])
        
    async def send_personal_message_json(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            
    async def broadcast_json(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


class ConnectionWebsocket:
    def __init__(self):
        """
        Crea una Lista de WebSocket
        """
        self.active_connections: dict = {}

    async def connect(self, id_connect: str,  websocket: WebSocket):
        """
        Agrega a la lista los usuarios conectados 
        """
        await websocket.accept()
        self.active_connections[f"{id_connect}"]                        = websocket
        print(self.active_connections) 

    def disconnect(self, id_connect: str):
        """ 
        Elimina a la lista los usuarios conectados 
        """
        self.active_connections.pop(f"{id_connect}")
        print(self.active_connections)

    async def send_private(self, id_connect: str, message: str):
 
        websocket = self.active_connections.get(f"{id_connect}", None)
        print(websocket)
        if websocket is not None:
            await websocket.send_json({"user_id": id_connect, "message": message})
        else:
            return False
            
        
        
    async def send_list_users(self, id_connect: str):
        print("id_connect", id_connect)
        websocket = self.active_connections.get(f"{id_connect}")
        users = list(self.active_connections.keys())
        print(users)
        await websocket.send_json({"users": users})

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await self.active_connections[connection].send_json(message)

