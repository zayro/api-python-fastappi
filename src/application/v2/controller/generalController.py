"""Imports."""

import json

from pydantic import ValidationError
from src.domain.model.search_model import Search
from src.domain.model.request_model import RequestResponse
from typing import Optional
from src.infrastructure.log.logService import ic

from src.infrastructure.database.mariadb.db import Database

""" import sys
sys.path.append('..')
 """


def search_controller(data: Search):
    """Esta Fucion permite Acceder al login ."""
    try:
        db = Database("astgu")
        print("enter a search_controller", data)

        ic(data)

        # Search User

        info = db.search_query(**data.model_dump())

        return {"success": True, "data": info, "code": 200}

    except ValidationError as e:
        print(e.errors())
        return {"success": False, "info": e.errors(), "code": 422}
