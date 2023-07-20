from src.service.datetimeService import time_to_seconds


def cache(**arg_decorador):
    def decorador_function(funcion: any):
        def change_function():
            response = funcion()
            second_time = time_to_seconds(**arg_decorador)
            headers = {"header": {"Cache-Control": "max-age=" + str(second_time)}}
            response.update(headers)
            return response

        return change_function

    return decorador_function


def cache_func_arg(**arg_decorador):
    def decorador_function(funcion: any):
        def change_function(**kwargs):
            response = funcion(**kwargs)
            second_time = time_to_seconds(**arg_decorador)
            headers = {"Cache-Control": "max-age=" + str(second_time)}
            kwargs.update(headers)
            print(arg_decorador)
            print(kwargs)
            return funcion(**kwargs)

        return change_function

    return decorador_function
