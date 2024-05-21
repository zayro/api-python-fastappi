from fastapi import HTTPException


def custom_http_exception(status_code: int, detail: str, headers: dict = None):
    """
    Crea una excepción HTTP personalizada.

    Args:
        status_code (int): Código de estado HTTP.
        detail (str): Detalle de la excepción.
        headers (dict, optional): Cabeceras adicionales. Por defecto es None.

    Returns:
        HTTPException: Excepción HTTP personalizada.
    """
    return HTTPException(status_code=status_code, detail=detail, headers=headers)
