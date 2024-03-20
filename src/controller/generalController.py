"""Imports."""

import json
from pydantic import ValidationError
from src.model.searchModel import Search
from database.postgredb.db_pg_medoo import Database

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

        info = search_query(data.query, data.fields)

        return {"success": True, "data": json.loads(info), "code": 200}

    except ValidationError as e:
        print(e.errors())
        return {"success": False, "info": e.errors(), "code": 422}


try:
    info = Search(query="demo.prueba", fields=["*"])
    # query="demo.prueba", fields=["*"]
    # info = {"query": "demo.prueba", "fields": ["*"]}

    search_controllers(data=info)
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))
    print(exc.errors())
