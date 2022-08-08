from fastapi import  Depends, APIRouter
from src.model.search import Search
from src.model.request import Insert
from src.db.general import Database
 

import src.controller.controllerHttp as controllerHttp
from src.middleware.token import validate_current_token

 
demo = Database('demo')

general = APIRouter(
    prefix="/api/v1/general",    
    responses={404: {"description": "Not found"}}
)

# SEARCH GENERAL SQL
@general.post("/search", dependencies=[Depends(validate_current_token)])
async def search(data: Search):
    demo.connectar();  

    if data.where is not None: 
         info = demo.search(data.fields, data.table, data.where)
    else: 
        info = demo.search(data.fields, data.table)
    return info

# INSERT GENERAL SQL
@general.post("/insert")
async def insert(data: Insert):
    response, message = demo.insert(data.insert, data.values)
    return controllerHttp.HttpResponse(response, message)
    