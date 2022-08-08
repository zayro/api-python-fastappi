from pydantic import BaseModel

class Search(BaseModel): 
    table: str
    fields: list | str
    where: dict | None
    
