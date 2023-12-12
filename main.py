"""RUN PROJECT."""
import uvicorn
from fastapi import Body, FastAPI, HTTPException, Request, Response, Request, status, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi_etag import add_exception_handler


import time
from src.service.websocketService import ConnectionManager, ConnectionWebsocket
import json

# Routes

from src.router.auth import auth
from src.router.general import general
from src.router.query import query
from src.router.view import view

# INIT APP
app = FastAPI()
add_exception_handler(app)

manager = ConnectionManager()
connectionWebsocket = ConnectionWebsocket()


@app.middleware("http")
async def add_cache_headers(request: Request, call_next) -> Response:
    print("validate middleware")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
def startup_event():
    print('start app')


@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


app.mount("/public", StaticFiles(directory="public"), name="public")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("----- Throw validation_exception_handler  ----")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"Error": exc.errors(), "Body": exc.body}),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    # return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
    print("----- Throw http_exception_handler  ----")
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc.detail),
    )


app.include_router(auth)
app.include_router(general)
app.include_router(view)
app.include_router(query)


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/api/v1")
async def root():
    return {"api": "v1"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
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


@app.websocket("/ws/json/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connectionWebsocket.connect(client_id, websocket)
    try:
        while True:
            print(f"info user #{client_id}")

            data = await websocket.receive_json()

            user_broadcast = data.get('broadcast', None)
            user_message = data.get('message', None)

            if (user_broadcast is not None):

                await connectionWebsocket.send_private(user_broadcast, user_message)
                info = {"user": client_id, "message": user_message}
                await connectionWebsocket.broadcast(info)
                print(f"Connect Client #{client_id}")

            if (data.get('listUser', None) is not None):
                print("listUser", client_id)
                await connectionWebsocket.send_list_users(client_id)

            if (data.get('private', None) is not None and data.get('user_id', None) is not None):
                await connectionWebsocket.send_private(data.get('user_id'), data.get('message'))

    except WebSocketDisconnect:
        connectionWebsocket.disconnect(client_id)
        await connectionWebsocket.broadcast(f"Client #{client_id} Disconnect")
        print(f"Disconnect Client #{client_id}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
