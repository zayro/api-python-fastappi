# main.py
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from infrastructure.websocket.websocketService import (
    ConnectionManager,
    ConnectionWebsocket,
)

manager = ConnectionManager()
connectionWebsocket = ConnectionWebsocket()


socket = APIRouter(prefix="/ws/v1", responses={404: {"description": "Not found"}})


@socket.websocket("/text/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """WebSocket text."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
            print(f"Connect Client #{client_id}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} Disconnect")
        print(f"Disconnect Client #{client_id}")


@socket.websocket("/json/{client_id}")
async def websocket_endpoint_json(websocket: WebSocket, client_id: str):
    """WebSocket Json."""
    try:
        while True:
            now = datetime.now()
            users = connectionWebsocket.get_list_users()
            print("connect ws", client_id, "\n")

            if len([item for item in users if item["user"] == client_id]) == 0:
                print("user:", client_id, "list users:", users, "\n")
                await connectionWebsocket.connect(client_id, now, websocket)
                info_connect_user = {"user": client_id, "message": "User Connected"}
                await connectionWebsocket.broadcast(info_connect_user)
                print(f"Connect User:  {client_id}")
            else:
                print("user exist:", client_id, "list users:", users, "\n")
                # await websocket.close(reason="user connect yet")

            data = await websocket.receive_json()

            user_broadcast = data.get("broadcast", None)
            user_message = data.get("message", None)
            message_private = data.get("private", None)
            user_id = data.get("user_id", None)
            list_user = data.get("listUser", None)
            update_user = data.get("updateUser", None)

            if user_broadcast is not None:
                await connectionWebsocket.send_private(client_id, user_message)
                info = {"user": client_id, "message": user_message}
                await connectionWebsocket.broadcast(info)
                print(f"Connect Client #{client_id}")

            if list_user is not None:
                await connectionWebsocket.send_list_users(client_id)

            if message_private is not None and user_id is not None:
                await connectionWebsocket.send_private(user_id, user_message)

            if update_user is not None:
                await connectionWebsocket.add_info_connect(
                    find=client_id, value=update_user
                )

    except WebSocketDisconnect:
        connectionWebsocket.disconnect(client_id)
        info_connect_user = {"user": client_id, "message": "User Disconnected"}
        await connectionWebsocket.broadcast(info_connect_user)
        print(f"Disconnect Client: {client_id}")
