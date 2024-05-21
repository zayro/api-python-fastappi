from pydantic import BaseModel


class RequestResponse(BaseModel):
    success: bool
    data: list | dict = None
    info: dict | None = None
    code: int = None
