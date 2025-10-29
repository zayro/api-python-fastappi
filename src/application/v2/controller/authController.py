"""
import sys
sys.path.append('..')
"""

import json
from icecream import ic
from src.domain.model.auth_model import Login

from src.infrastructure.database.mariadb.db import Database

from src.utils.bcrypt_utils import verify_password
from src.infrastructure.security.jwt_handler import JWTHandler


def login_controller(data: Login):
    """Esta Fucion permite Acceder al login ."""
    try:
        print("ingreso a loginController")

        # Search User

        db = Database("accessgu")

        # Acceso a base de datos de astgu
        rs = db.search_query(
            query="acceso_empleados",
            fields=["password", "email", "identificacion"],
            where={"identificacion": data.username},
        )

        # Acceso a base de datos de astgu
        db = Database("astgu")
        empleados = db.search_query(
            query="vlpempleados",
            fields=["idlpempleado", "nroidentificacion", "nombrecompleto", "email", "activo"],
            where={"nroidentificacion": data.username},
        )

        jwt_handler = JWTHandler()

        ic(rs)

        print(type(rs))

        # info = json.loads(rs)
        info = rs
        empleados_info = empleados

        # Valid if exist user
        if len(info) > 0:
            # Valid if password it's match
            if verify_password(data.password, info[0].get("password")):
                print("creando token")
                token = jwt_handler.create_token(
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
                        "nombrecompleto": empleados_info[0].get("nombrecompleto"),
                        "idlpempleado": empleados_info[0].get("idlpempleado"),
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

    except Exception as error:
        print("----- Exception loginController ----- ")
        ic(error)
        raise RuntimeError("An error occurred while executing the login_controller") from error
