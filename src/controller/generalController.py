"""Imports."""
import json
from pydantic import ValidationError
from src.model.search import Search
from src.db.general import Database
from src.tools.messageResponse import message_type_error, message_exception_error
""" import sys
sys.path.append('..')
 """


def search_controller(data: Search):
    """Esta Fucion permite Acceder al login ."""
    try:
        db = Database()
        print("ingreso a search_controller")

        # Search User
        if data.where is not None:
            info = db.search(data.table, data.fields,
                             data.where).export("json")
        else:
            info = db.search(data.table, data.fields).export("json")

        return {"success": True, "data": json.loads(info), "info": {}}

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        message_exception_error(e, "search_controller")
        return {"success": False,
                "data": [],
                "info": {
                    "error": "Error al formar Sql",
                    "message": type(e).__name__
                }
                }
    except ValidationError as e:
        print(e.errors())
    finally:
        db.close()