from pydantic import BaseModel

class Insert(BaseModel): 
    insert: str
    values: list[dict]

    
