from pydantic import BaseModel


class RequestResponse(BaseModel):
    data: list[dict] | None = []
    success: bool
    info: dict | None = {}
    code: int
