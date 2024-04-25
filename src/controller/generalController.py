"""Imports."""

import json
from src.service.logService import ic
from pydantic import ValidationError
from src.model.searchModel import Search
from src.database.postgredb.db_pg_medoo import Database

from src.database.postgredb.connect import search_query

""" import sys
sys.path.append('..')
 """


def search_controller(data: Search):
    """Esta Fucion permite Acceder al login ."""
    try:
        db = Database()
        print("enter a search_controller", data)

        # Search User
        if data.where is not None:
            info = db.search(data.query, data.fields, data.where).export("json")
        else:
            info = db.search(data.query, data.fields).export("json")

        # print log last sql
        db.log()
        db.error()

        return {"success": True, "data": json.loads(info), "code": 200}

    except ValidationError as e:
        print(e.errors())
        return {"success": False, "info": e.errors(), "code": 422}

    finally:
        db.close()


def search_controllers(data: Search):
    """Esta Fucion permite Acceder al login ."""
    try:

        ic(data.model_dump())

        info = search_query(**data.model_dump())

        return {"success": True, "data": json.loads(info), "code": 200}

    except ValidationError as e:
        ic(e.errors())
        return {"success": False, "info": e.errors(), "code": 422}
