""" Service."""

import traceback
from datetime import datetime
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


""" WebSocket Route Json"""


class ConnectionWebsocket:
    users: list = []

    def __init__(self):
        """
        Crea una Lista de WebSocket
        """
        self.active_connections: dict = {}

    async def connect(self, id_connect: str, time_start: str, websocket: WebSocket):
        """
        Agrega a la lista los usuarios conectados
        """
        await websocket.accept()
        current_user = {
            "user": f"{id_connect}",
            "history": [
                {
                    "module": "init session",
                    "time_start": f"{time_start}",
                }
            ],
        }
        self.active_connections[f"{id_connect}"] = websocket
        self.users.append(current_user)

        print("Current User", self.users, "\n")

    def disconnect(self, id_connect: str):
        """Elimina a la lista los usuarios conectados"""
        try:
            print("disconnect", id_connect, "\n")
            self.active_connections.pop(f"{id_connect}")

            find_user_discard = self.find_user_discard(
                find=id_connect, find_by="user", list_dict=self.users
            )

            # self.users.clear()

            self.users = find_user_discard

            print("users", self.users, "\n")

        except ValueError:
            print("That item does not exist")

    def find_connect(self, find, find_by, list_dict):
        return_element = [
            element for element in list_dict if element[f"{find_by}"] == find
        ]
        return return_element

    def update_user_module(self, find, value):
        self.update_user_connect(
            find_by="user",
            find=find,
            value_update=value,
            list_dict=self.users,
            attribute="module",
        )

    def find_user_discard(self, find, find_by, list_dict):
        return_element = [
            element for element in list_dict if element[f"{find_by}"] != find
        ]
        return return_element

    def delete_user_connect(self, list_dict: list, find_by, find):
        for item in list_dict:
            if item[find_by] == find:
                list_dict.remove(item)

    async def add_info_connect(self, find: str, value: dict):
        try:
            print("ingreso al metodo")
            now = datetime.now()
            # Lista comprimida
            return_new_list = [
                element for element in self.users if element.get("user") == find
            ]

            if len(return_new_list) != 0:
                for element in return_new_list:
                    # Actualiza dinámicamente el atributo especificado
                    print(len(element["history"]), "cantidad elementos", "\n")
                    print(element["history"][-1], "ultimo elemento")
                    if len(element["history"]) > 0:
                        element["history"][-1].update({"time_end": f"{now}"})

                    value["time_start"] = f"{now}"
                    element["history"].append(value)

            else:
                print("lista vacia")

            # Devuelve la lista actualizada o la original si no hubo cambios

        except NameError:
            print("Variable it's not defined")
        except ValueError:
            print("That item does not exist")
        except Exception as e:
            print("error no controlado", e)
            traceback.print_exc()

    def update_user_connect(
        self, find: str, find_by: str, list_dict: list, value_update, attribute: str
    ):
        # Lista comprimida
        return_new_list = [
            element for element in list_dict if element.get(find_by) == find
        ]

        if return_new_list:
            for element in return_new_list:
                # Actualiza dinámicamente el atributo especificado
                element[attribute] = value_update

        # Devuelve la lista actualizada o la original si no hubo cambios
        return return_new_list or list_dict

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
        await websocket.send_json({"users": self.users})

    def get_list_users(self):
        return self.users

    def get_list_connect(self):
        return self.active_connections

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await self.active_connections[connection].send_json(message)
