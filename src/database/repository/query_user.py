"""
The code defines functions to connect to a PostgreSQL database, execute SQL queries, retrieve data,
and insert data, with error handling and JSON conversion capabilities.
:return: The `max_seq_table` function is returning the result of a SQL query that finds the maximum
value of the field "id_users" in the "auth.users" table and increments it by 1. The result is
returned as a dictionary containing the incremented value under the key "id_users".
"""

import psycopg2.extras
from pydantic import ValidationError
from src.service.logService import ic
from src.model.authModel import Login
from src.model.userModel import UserPasswordChange
from src.database.postgredb.connect import connect, execute_sql
from src.tools.convert import sql_data
from src.tools.toolsBcript import checkPasswd, createPasswd


def auth_user(login: Login) -> dict:
    """Execute Sql Postgresql"""
    ic(login)
    sql = """ SELECT email, username, password FROM auth.users WHERE username = %s """
    return execute_sql(sql, [login.username])


def update_password_user(data: UserPasswordChange) -> dict:
    """Execute Sql Postgresql"""

    sql = """ SELECT email, username, password FROM auth.users WHERE email = %s """

    response_sql: dict = execute_sql(sql, [data.email])

    ic(type(response_sql))
    ic(response_sql)

    if checkPasswd(data.oldPassword, response_sql.get("data")[0].get("password")):

        data.newPassword = createPasswd(data.newPassword)
        params: dict = {
            "email": data.email,
            "newPassword": data.newPassword,
            "oldPassword": response_sql.get("data")[0].get("password"),
        }
        sql = """ UPDATE auth.users SET password = %(newPassword)s  WHERE email = %(email)s  RETURNING email, username """
        return execute_sql(sql, params)
    else:
        return {
            "success": False,
            "message": "Password no coincide",
            "error": "Password no coincide",
        }


def create_user(payload_user: dict) -> dict:
    """Execute Sql Postgresql"""

    try:
        with connect() as conn:

            conn.autocommit = False

            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

                sql_max_id_field_user = (
                    """SELECT MAX(id_users) + 1 as id_users FROM auth.users """
                )

                cur.execute(sql_max_id_field_user)

                execute_max_id_field_user = cur.fetchone()

                ic(payload_user)

                payload_user.update(execute_max_id_field_user)

                sql_insert_user = """INSERT INTO auth.users (id_users, username, password, email) VALUES (%(id_users)s, %(username)s, %(password)s, %(email)s) RETURNING id_users"""

                cur.execute(sql_insert_user, payload_user)

                execute_insert_user = sql_data(cur.fetchall())[0]

                ## second query

                sql_max_id_field_users_validation = """SELECT MAX(id_users_validation) + 1 as id_users_validation FROM auth.users_validation """

                cur.execute(sql_max_id_field_users_validation)

                payload_user_validation = {
                    "id_users_roles": 2,
                    "status": 1,
                    "verified": False,
                }

                execute_max_id_field_user_validation = cur.fetchone()

                payload_user_validation.update(execute_insert_user)

                payload_user_validation.update(execute_max_id_field_user_validation)

                sql_insert_user_validation = """INSERT INTO auth.users_validation (id_users_validation, id_users_roles, id_users, status, verified) VALUES (%(id_users_validation)s, %(id_users_roles)s, %(id_users)s, %(status)s, %(verified)s) RETURNING id_users_validation"""

                cur.execute(sql_insert_user_validation, payload_user_validation)

                conn.commit()
                ic("Transaction completed successfully create user ")

                response_to_controller: dict = {
                    "success": True,
                    "message": "se ejecuto Exitosamente",
                }

                return response_to_controller

    except (psycopg2.DatabaseError, ValidationError) as error:
        ic(error)
        conn.rollback()
        return {
            "success": False,
            "message": "Error al ejecutar la consulta",
            "error": str(error),
        }
