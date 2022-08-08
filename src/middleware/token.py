
from fastapi import Request, HTTPException
from src.controller.controllerToken import validate_token
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()
        
        async def verify_token_middleware(request:Request):
            try:
                token = request.headers["Authorization"].split(" ")[1]
                print(token)
                print("---------------------------")
                validation_response = validate_token(token, output=False)
                print("---------------------------")
                print(validation_response)
                if validation_response == None:
                    return await original_route(request)
                else:
                    return validation_response 
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)            


        return verify_token_middleware