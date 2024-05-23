"""Imports."""

import json

from pydantic import ValidationError
from src.domain.model.search_model import Search
from src.domain.model.request_model import RequestResponse
from src.infrastructure.database.orm.db_pg_medoo import Database
from src.infrastructure.log.logService import ic
from src.infrastructure.database.postgredb.connect import search_query

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


def search_controllers(data: Search) -> RequestResponse:
    """Esta Fucion permite Acceder al login ."""
    try:

        ic(data.model_dump())

        info: dict = search_query(**data.model_dump())

        info.update({"code": 200})

        ic(info)

        return info

    except ValidationError as e:
        ic(e.errors())
        return {"success": False, "info": e.errors(), "code": 422}
