"""
The code defines functions to connect to a PostgreSQL database, execute SQL queries, retrieve data,
and insert data, with error handling and JSON conversion capabilities.
:return: The `max_seq_table` function is returning the result of a SQL query that finds the maximum
value of the field "id_users" in the "auth.users" table and increments it by 1. The result is
returned as a dictionary containing the incremented value under the key "id_users".
"""

import sys
from typing import Optional
import psycopg2.extras
from infrastructure.log.logService import ic
from src.tools.sql import SqlTools
from src.tools.convert import sql_data
from config.settings import Enviroment


def connect():
    """Connect to the PostgreSQL database server"""
    try:
        # Definición de parámetros de conexión

        env = Enviroment()

        host = env.db_host
        database = env.db_name
        user = env.db_user
        password = env.db_pass

        # connecting to the PostgreSQL server
        with psycopg2.connect(
            host=host, database=database, user=user, password=password
        ) as conn:
            print("Connected to the PostgreSQL server.")
            # Cierra el cursor (no necesario dentro del context manager)
            # cur.close()

            return conn
        # La conexión se cierra automáticamente al salir del bloque `with`
    except (Exception, psycopg2.DatabaseError, TypeError) as e:
        print("----- Exception General Database ----- ")
        print(
            type(e).__name__,  # TypeError
            __file__,  # /tmp/example.py
            e.__traceback__.tb_lineno,  # 2
        )
        print(str(e))
        print("---------- ")
        sys.exit()
        # muestra si existen errores
    finally:
        # Cierra el cursor (no necesario dentro del context manager)
        # cur.close()

        # Verifica si la conexión se cerró correctamente
        if conn is not None and conn.closed != 1:
            print("Conexion cerrada exitosamente")
        else:
            print("Error al cerrar la conexion")


def execute_sql(
    sql: str, params: Optional[list] = None, autocommit: Optional[bool] = True
) -> dict:
    """Execute Sql Postgresql"""
    try:
        with connect() as conn:

            conn.autocommit = autocommit
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, params)
                print("The number of result: ", cur.rowcount)
                json_data = sql_data(cur.fetchall())
                # ic(json_data)
                cur.close()

                return {
                    "success": True,
                    "data": json_data,
                }

    except (psycopg2.DatabaseError, TypeError) as error:
        ic(error)
        return {
            "success": False,
            "message": "Error al ejecutar la consulta",
            "error": str(error),
        }


def max_seq_table(
    table: str,
    field: str,
):
    """Retrieve data from the  table"""
    sql = f"select max({field}) + 1 as {field} from {table}; "
    ic(sql)
    try:
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql)
                result = cur.fetchone()
                return result

    except psycopg2.DatabaseError as error:
        print(error)


def search_query(
    query: str,
    fields: list,
    where: Optional[dict] = None,
    order: Optional[dict] = None,
    limit: Optional[int] = None,
):
    """Retrieve data from the  table"""

    sql_tools = SqlTools("pg")

    sql = sql_tools.select(
        table=query, fields=fields, where=where, order=order, limit=limit
    )

    ic(sql)
    return execute_sql(sql)


def insert_query(table: str, data_insert: dict):
    """Insert data from the  table"""

    sql_tools = SqlTools("pg")

    sql = sql_tools.generate_insert_query(table_name=table, data=data_insert)

    ic(sql)

    try:
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql)
                print("The number of result: ", cur.rowcount)

                cur.close()

                return {"success": True, "message": "se ejecuto Exitosamente"}

    except psycopg2.DatabaseError as error:
        ic(error)
        return {
            "success": False,
            "message": "Error al ejecutar la consulta",
            "error": str(error),
        }
