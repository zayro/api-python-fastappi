
from fastapi import FastAPI, Request, status

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import time
from src.router.general import general

app = FastAPI()
 
@app.on_event("startup")
async def startup_event():
    print('start app')

@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")




@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"Error": exc.errors(), "Body": exc.body}),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    #return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc.detail),
    )

app.include_router(general)



@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
