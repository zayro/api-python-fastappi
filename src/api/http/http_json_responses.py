from fastapi.responses import JSONResponse


def custom_json_response(content: dict, status_code: int = 200, headers: dict = None):
    """
    Crea una respuesta JSON personalizada.

    Args:
        content (dict): Contenido de la respuesta JSON.
        status_code (int, optional): Código de estado HTTP. Por defecto es 200.
        headers (dict, optional): Cabeceras adicionales. Por defecto es None.

    Returns:
        JSONResponse: Respuesta JSON personalizada.
    """
    return JSONResponse(content=content, status_code=status_code, headers=headers)
