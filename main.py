"""RUN PROJECT."""

import uvicorn
from fastapi import Body, FastAPI, HTTPException, Request, Response, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi_etag import add_exception_handler
from fastapi.middleware.cors import CORSMiddleware

import time
from datetime import datetime

# Routes
from src.router.auth import auth
from src.router.general import general
from src.router.query import query
from src.router.view import view
from src.router.cache import cache
from src.router.pdf import pdf
from src.router.upload import upload
from src.router.files import files
from src.router.webSocket import socket

# INIT APP
app = FastAPI()

tags_metadata = [
    {"name": "Consulta", "description": "Metodos que permiten consultar"},
    {"name": "Get Methods", "description": "Permite Consultar"},
    {"name": "Post Methods", "description": "Ingresar Nueva Informacion"},
    {"name": "Delete Methods", "description": "Eliminar Registros"},
    {"name": "Put Methods", "description": "Actualizar Informacion"},
]

app = FastAPI(
    title="ApiBackendApp",
    description="Api que permite manejo informacion de la base de datos",
    version="0.0.1",
    openapi_tags=tags_metadata,
)


add_exception_handler(app)


@app.middleware("http")
async def add_cache_headers(request: Request, call_next) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    print("start app")
    start_time = datetime.now()
    with open("src/log.txt", mode="a") as log:
        log.write(f"--  \n")
        log.write(f"Application Start: {start_time}\n")
        log.close()


@app.on_event("shutdown")
def shutdown_event():
    start_time = datetime.now()
    with open("src/log.txt", mode="a") as log:
        log.write(f"Application shutdown: {start_time}\n")
        log.close()


app.mount("/public", StaticFiles(directory="public"), name="public")

# Exception of project

"""
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("----- Throw validation_exception_handler  ----")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"success": False, "info": exc.errors(), "Body": exc.body}
        ),
    )
    
"""


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    # return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
    print("----- Throw http_exception_handler  ----")
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"success": False, "info": exc.detail}),
    )


"""
* Routes of project
"""

app.include_router(auth)
app.include_router(general)
app.include_router(view)
app.include_router(query)
app.include_router(cache)
app.include_router(pdf)
app.include_router(upload)
app.include_router(files)
app.include_router(socket)


@app.get("/")
async def root():
    return {"api": "v1"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
