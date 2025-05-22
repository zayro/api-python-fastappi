def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("----- Exception in function:", func.__name__, "-----")
            print(type(e).__name__, e)
            return {
                "success": False,
                "data": [],
                "info": {"message": str(e)},
                "code": 500,
            }
    return wrapper