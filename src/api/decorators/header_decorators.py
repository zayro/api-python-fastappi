from functools import wraps
from fastapi import Response


def add_custom_headers(headers: dict):
    """
    Decorador para agregar cabeceras personalizadas a una respuesta de FastAPI.

    Args:
        headers (dict): Un diccionario de cabeceras a agregar.

    Returns:
        function: Decorador que agrega las cabeceras personalizadas a la respuesta.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Llamar a la función original para obtener la respuesta
            response = await func(*args, **kwargs)
            # Verificar si la respuesta es un objeto Response
            if isinstance(response, Response):
                # Agregar las cabeceras personalizadas
                for key, value in headers.items():
                    response.headers[key] = value
            return response

        return wrapper

    return decorator
