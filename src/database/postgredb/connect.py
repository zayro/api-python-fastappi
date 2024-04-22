"""connect database """

import sys
import json
from icecream import ic
import datetime
from typing import Optional
import psycopg2.extras


from config.settings import Enviroment
from src.tools.sql import SqlTools


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


def execute_sql(sql: str):
    """Retrieve data from the  table"""

    ic(sql)

    try:
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql)
                result = cur.fetchone()
                return result

    except psycopg2.DatabaseError as error:
        print(error)


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
    table: str,
    fields: list,
    where: Optional[dict] = None,
    order: Optional[dict] = None,
    limit: Optional[int] = None,
):
    """Retrieve data from the  table"""

    sql_tools = SqlTools("pg")

    sql = sql_tools.select(
        table=table, fields=fields, where=where, order=order, limit=limit
    )

    ic(sql)

    try:
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql)
                print("The number of result: ", cur.rowcount)
                result = []
                for row in cur.fetchall():
                    result.append(
                        {key: convertir_a_json(value) for key, value in row.items()}
                    )

                json_data = json.dumps(result, sort_keys=True)
                ic(json_data)
                cur.close()

                return json_data

    except psycopg2.DatabaseError as error:
        print(error)


def insert_query(table: str, data_insert: dict):
    """Retrieve data from the  table"""

    sql_tools = SqlTools("pg")

    sql = sql_tools.insert(table=table, data=data_insert)

    ic(sql)

    try:
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql)
                print("The number of result: ", cur.rowcount)

                cur.close()

                return {"message": "se ejecuto Exitosamente"}

    except psycopg2.DatabaseError as error:
        print(error)


def convertir_a_json(valor):
    ic(valor)
    if isinstance(valor, datetime.datetime):
        return valor.isoformat()
    elif isinstance(valor, bytes):
        return valor.decode("utf-8")
    elif isinstance(valor, dict):
        return {key: convertir_a_json(v) for key, v in valor.items()}
    elif isinstance(valor, list):
        return [convertir_a_json(v) for v in valor]
    else:
        return valor


def prueba_query():

    query_table = "demo.prueba"
    query_fields = ["id", "name"]
    limit_fields = 1

    rows = search_query(table=query_table, fields=query_fields, limit=limit_fields)

    print(rows)


res = max_seq_table("auth.users", "id_users")
print(res)
