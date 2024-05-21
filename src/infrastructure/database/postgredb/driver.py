"""
the code is a simple example of how to use a database connection in FastAPI using a dependency.
"""

from contextlib import contextmanager
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

# from src.service.logService import ic

# Configuración de la base de datos PostgreSQL
DATABASE_CONFIG = {
    "host": "localhost",
    "database": "enterprise",
    "user": "postgres",
    "password": "zayro",
}


# Función de dependencia para obtener una conexión de base de datos


@contextmanager
def get_db():
    """
    Dependencia para obtener una conexión de base de datos PostgreSQL.

    Esta función crea una conexión de base de datos, la devuelve para su uso en una petición
    y luego cierra la conexión y realiza una limpieza al finalizar la petición.

    Yields:
        cursor: Cursor de base de datos para usar en la petición.
    """
    # Crear una conexión a la base de datos PostgreSQL
    connection = psycopg2.connect(**DATABASE_CONFIG)

    # Usar un cursor que devuelve los resultados como diccionarios
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    try:
        # Retornar el cursor para su uso
        yield cursor
    except (psycopg2.DatabaseError, TypeError) as e:
        print(e)
        sys.exit()
    finally:
        # Cerrar el cursor y la conexión para limpiar recursos
        cursor.close()
        connection.close()


def get_all_items():
    """
    Obtiene todos los items de la base de datos.
    """
    # Consulta SQL para obtener todos los items
    select_query = "SELECT email, username, password FROM auth.users;"
    try:
        get_db.execute(select_query)
        items = get_db.fetchall()
        print(items)
    except (psycopg2.DatabaseError, TypeError) as e:
        print(e)

    return items


get_all_items()
