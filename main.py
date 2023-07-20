"""RUN PROJECT."""
import uvicorn
from fastapi import FastAPI, Request, status, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles

from src.redis.connect import cache_redis

# Routes

from src.router.auth import auth
from src.router.general import general
from src.router.query import query
from src.router.view import view

# INIT APP
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print('start app')
    cache_redis()


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


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
