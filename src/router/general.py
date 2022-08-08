from fastapi import  Depends, APIRouter, HTTPException, status

from src.model.search import Search
from src.model.request import Insert
from src.db.general import Database
 
from src.controller.controllerToken import write_token, validate_token
from src.tools.toolsBcript import checkPasswd
import src.controller.controllerHttp as controllerHttp

from fastapi.security import OAuth2PasswordBearer
import jwt


from multiprocessing import Process

general = APIRouter(
    prefix="/api/v1/general",    
    responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def validate_current_token(token: str = Depends(oauth2_scheme)):
    
    try: 
         token = validate_token(token)
         
         print(token)
         
    except jwt.exceptions.DecodeError as e:
        print("-------------------", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error: {e}",
            headers={"WWW-Authenticate": "Bearer"},)
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error: {e}",
            headers={"WWW-Authenticate": "Bearer"},)     
    except jwt.exceptions.InvalidSignatureError as e:
        print (e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error: {e}",
            headers={"WWW-Authenticate": "Bearer"},)     
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error: {e}",
            headers={"WWW-Authenticate": "Bearer"},)

auth = Database('auth')
demo = Database('demo')



@general.post("/login")
async def login():

    username = 'zayrosf'
    password = '123456'    

    cursor = auth.connectar();     
    
    cursor.execute('Select username, password From users Where username = ? or email = ?', [username, password])
    
    cursor = auth.connectar();     
    
    cursor.execute('Select username, password From users Where username = ? or email = ?', [username, password])    
    
          
    count = cursor.rowcount

    
    if count > 0:
        for (user, has) in cursor.fetchall(): 
            if checkPasswd(password, has):
                token = write_token({"username": user})
                return controllerHttp.HttpResponse(True, {"toke": token})

        return controllerHttp.HttpResponse(False, "Not Match Pass")
    else : 
        return controllerHttp.HttpResponse(False, "Not Found Rows")

@general.post("/search", dependencies=[Depends(validate_current_token)])
async def search(data: Search):
    demo.connectar();  

    if data.where is not None: 
         info = demo.search(data.fields, data.table, data.where)
    else: 
        info = demo.search(data.fields, data.table)
    return info

@general.post("/insert")
async def insert(data: Insert):
    db = Database('demo')
    response, message = db.insert(data.insert, data.values)
    return controllerHttp.HttpResponse(response, message)
    