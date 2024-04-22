import json
from icecream import ic
from src.model.userModel import User
from src.database.postgredb.connect import insert_query, max_seq_table


def new_user_controller(data: User):
    """Esta Fucion permite Acceder al login ."""
    try:

        # Search User
        result_body_json = dict((x, y) for x, y in data)

        max = max_seq_table(table="auth.users", field="id_users")

        result_body_json.update(max)

        ic(result_body_json)

        rs = insert_query(table="auth.users", data_insert=result_body_json)

        ic(rs)

        info = json.loads(rs)

        # Valid if exist user
        if len(info) > 0:

            return {
                "success": True,
                "data": {},
                "info": {},
                "code": 200,
            }

        else:
            return {
                "success": False,
                "data": [],
                "info": {"message": "not match username"},
                "code": 401,
            }

    except Exception as e:
        ic(e)
        print(
            type(e).__name__,
            __file__,
            e,
        )
        print(str(e))
        print("---------- ")
        return "error"
