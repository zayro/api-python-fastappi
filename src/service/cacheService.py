from src.service.datetimeService import time_to_miliseconds
from email.utils import formatdate
from datetime import datetime, timedelta
def cache(**arg_decorador):
    def decorador_function(funcion: any):
        def change_function():
            response = funcion()
            second_time = time_to_miliseconds(**arg_decorador)
            # Obtenga la hora actual
            now = datetime.now()
            # Agregue una hora a la hora actual
            later = now + timedelta(**arg_decorador)          
            etag =  f'W/"cached"'
            #response.headers["ETag"] = etag
            #response.headers["Last-Modified"] = formatdate(timeval=None, localtime=False, usegmt=True)
            #response.headers["Cache-Control"] = "public, max-age=" + str(second_time)
            headers = {
                "header": {
                   # "Cache-Control": "public, must-revalidate, max-age=" + str(second_time),
                    "Cache-Control": "public, must-revalidate",
                    "Expires": formatdate(timeval=later.timestamp(), localtime=False, usegmt=True),                     
                    "Last-Modified": formatdate(timeval=None, localtime=False, usegmt=True),
                    #"ETag": etag
                    
                }
            }
            response.update(headers)
            return response

        return change_function

    return decorador_function


def cache_func_arg(**arg_decorador):
    def decorador_function(funcion: any):
        def change_function(**kwargs):
            response = funcion(**kwargs)
            second_time = time_to_miliseconds(**arg_decorador)
            headers = {"Cache-Control": "max-age=" + str(second_time)}
            kwargs.update(headers)
            print(arg_decorador)
            print(kwargs)
            return funcion(**kwargs)

        return change_function

    return decorador_function
