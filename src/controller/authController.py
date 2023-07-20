""" import sys

sys.path.append('..')
 """
import json
from src.model.auth import Login
from src.db.general import Database
from src.tools.toolsBcript import checkPasswd
from src.service.serviceToken import write_token


def login_controller(data: Login):
    """Esta Fucion permite Acceder al login ."""
    try:
        
        print("---- redis ----", r.ping())
        db = Database()
        print("ingreso a loginController")

        # Search User
        rs = db.search("auth.users", "*", where={"username": data.username}).export(
            "json"
        )

        info = json.loads(rs)

        # Valid if exist user
        if len(info) > 0:
            # Valid if password it's match
            if checkPasswd(data.password, info[0].get("password")):
                print("creando token")
                token = write_token(
                    {
                        "permissions": ["admin", "user:read", "user:write"],
                    }
                )
                return {"success": True, "data": [{"token": token}], "info": {}}
            else:
                return {
                    "success": False,
                    "data": [],
                    "info": {"message": "not match password"},
                }
        else:
            return {
                "success": False,
                "data": [],
                "info": {"message": "not match username"},
            }

    except Exception as e:
        print("----- Exception loginController ----- ")
        print(
            type(e).__name__,  __file__, e,
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
