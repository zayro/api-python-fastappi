from pydantic import BaseModel


class RequestResponse(BaseModel):
    data: list[dict] | None = None
    success: bool
    info: dict | None = None
    code: int
