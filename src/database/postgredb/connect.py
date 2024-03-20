"""connect database """

import sys
import json
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
    print(sql)

    try:
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(sql)
                print("The number of result: ", cur.rowcount)
                result = cur.fetchall()
                # Convertir las filas a JSON
                result_to_json = json.dumps([dict(row) for row in result])
                cur.close()

                return result_to_json

    except psycopg2.DatabaseError as error:
        print(error)


def prueba_query():

    query_table = "demo.prueba"
    query_fields = ["id", "name"]
    limit_fields = 10

    rows = search_query(table=query_table, fields=query_fields, limit=limit_fields)

    print(rows)


prueba_query()
