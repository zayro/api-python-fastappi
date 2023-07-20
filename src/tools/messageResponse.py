
def message_response(success: bool, data, info=None, code=None):
    """Return message formatter."""
    print(code)
    return {"success": success, "data": data, "info": info}

def message_response_object(success: bool, data, info=None, code=None):
    """Return message formatter."""
    print(code)
    return {"success": success, "data": data, "info": info}


def message_type_error(e):
    """Print Error."""
    print("----- TypeError ----- ")
    print(str(e))
    print("---------- ")


def message_exception_error(e, name: str | None):
    """Print Error."""
    print(f"----- Exception -----  {name}")
    print(type(e).__name__, __file__)
    print("---------- ")
    print("\n")
    print(str(e))
    print("---------- ")
