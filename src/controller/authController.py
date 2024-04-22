""" 
import sys
sys.path.append('..')
 """

import json
from icecream import ic
from src.model.authModel import Login
from src.database.postgredb.db_pg_medoo import Database
from src.database.postgredb.connect import search_query
from src.tools.toolsBcript import checkPasswd
from src.service.tokenService import write_token


def login_controller(data: Login):
    """Esta Fucion permite Acceder al login ."""
    try:

        ic()

        # Search User
        rs = search_query(
            table="auth.users",
            fields=["password", "email", "created_at"],
            where={"username": data.username},
        )

        ic(rs)

        info = json.loads(rs)

        # Valid if exist user
        if len(info) > 0:
            # Valid if password it's match
            if checkPasswd(data.password, info[0].get("password")):
                print("creando token")
                token = write_token(
                    {
                        "username": data.username,
                        "email": info[0].get("email"),
                        "permissions": ["admin", "user:read", "user:write"],
                    }
                )
                return {
                    "success": True,
                    "data": {
                        "token": token,
                        "username": data.username,
                        "email": info[0].get("email"),
                    },
                    "info": {},
                    "code": 200,
                }

            else:
                return {
                    "success": False,
                    "data": [],
                    "info": {"message": "not match password"},
                    "code": 401,
                }
        else:
            return {
                "success": False,
                "data": [],
                "info": {"message": "not match username"},
                "code": 401,
            }

    except Exception as e:
        print("----- Exception loginController ----- ")
        print(
            type(e).__name__,
            __file__,
            e,
        )
        print(str(e))
        print("---------- ")
        return "error"


def login_doc_controller(username, password):
    """Esta Fucion permite Acceder al login ."""
    try:
        db = Database()
        print("ingreso a loginController")

        # Search User
        rs = db.search("auth.users", "*", where={"username": username}).export("json")

        info = json.loads(rs)

        # Valid if exist user
        if len(info) > 0:
            # Valid if password it's match
            if checkPasswd(password, info[0].get("password")):
                print("creando token")
                token = write_token(
                    {
                        "username": username,
                        "email": info[0].get("email"),
                        "permissions": ["admin", "user:read", "user:write"],
                    }
                )
                return {"token": token}

            else:
                return {
                    "success": False,
                    "data": [],
                    "info": {"message": "not match password"},
                    "code": 401,
                }
        else:
            return {
                "success": False,
                "data": [],
                "info": {"message": "not match username"},
                "code": 401,
            }

    except Exception as e:
        print("----- Exception loginController ----- ")
        print(
            type(e).__name__,
            __file__,
            e,
        )
        print(str(e))
        print("---------- ")
        return "error"
    finally:
        db.close()


"""
info =  Login(username= 'zayrod', password= '123456')

login(info)

 
  """
