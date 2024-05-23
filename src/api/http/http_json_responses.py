from fastapi.responses import JSONResponse
from fastapi import status


def http_json_response(content: dict, status_code: int = 200, headers: dict = None):
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



def http_response_code(**data):
    """Response Request."""
    code = data.get("code", 500)
    header = data.get("header", {})

    if code == 200:
        status_code = status.HTTP_200_OK
    elif code == 201:
        status_code = status.HTTP_201_CREATED
    elif code == 202:
        status_code = status.HTTP_202_ACCEPTED
    elif code == 304:
        status_code = status.HTTP_304_NOT_MODIFIED
    elif code == 400:
        status_code = status.HTTP_400_BAD_REQUEST
    elif code == 401:
        status_code = status.HTTP_401_UNAUTHORIZED
    elif code == 404:
        status_code = status.HTTP_404_NOT_FOUND
    elif code == 405:
        status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    elif code == 408:
        status_code = status.HTTP_408_REQUEST_TIMEOUT
    elif code == 500:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif code == 501:
        status_code = status.HTTP_501_NOT_IMPLEMENTED
    elif code == 503:
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    data.pop("code")
    data.pop("header", {})

    return JSONResponse(status_code=status_code, content=data, headers=header)