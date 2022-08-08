from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates



view = APIRouter(
    prefix="/api/v1/view",    
    responses={404: {"description": "Not found"}}
)


templates = Jinja2Templates(directory="public/templates")


@view.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("info.html", {"request": request, "id": id})
