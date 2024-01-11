"""Imports."""
import json
from pydantic import ValidationError
from src.model.searchModel import Search
from src.db.general import Database

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
            info = db.search(data.query, data.fields,
                             data.where).export("json")
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
