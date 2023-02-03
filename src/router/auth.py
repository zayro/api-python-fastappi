from fastapi import APIRouter
from src.controller.controllerToken import write_token
from src.tools.toolsBcript import checkPasswd
import src.controller.controllerHttp as controllerHttp
from src.model.auth import Login
from src.db.general import Database

auth = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}}
)

db = Database('auth')


@auth.post("/login")
async def login(data: Login):

    username = data.username
    password = data.password

    cursor = db.connectar()

    cursor.execute('Select username, password From users Where username = ? or email = ?', [
                   username, password])

    count = cursor.rowcount

    if count > 0:
        for (user, has) in cursor.fetchall():
            if checkPasswd(password, has):
                token = write_token({"username": user,                                     
                                     "permissions": [
                                         "admin",
                                         "user:read",
                                         "user:write"
                                     ],
                                     })
                return controllerHttp.HttpResponse(True, {"token": token})

        return controllerHttp.HttpResponse(False, "Not Match Pass")
    else:
        return controllerHttp.HttpResponse(False, "Not Found Rows")
