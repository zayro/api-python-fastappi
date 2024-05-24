from fastapi import WebSocket


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
