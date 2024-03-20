"""Model Search"""

from pydantic import BaseModel


class Search(BaseModel): 
    """Clase Busqueda"""

    query: str
    fields: list | str
    where: dict | None = {}
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "demo.prueba", "fields": "*"},
                {
                    "from": "prueba",
                    "fields": ["id", "nombre"],
                    "order": [{"column": "id", "order": "desc"}],
                },
            ]
        }
    }


"""     @field_validator('where')
    def value_must_equal_bar(cls, v):
        if v != 'bar':
            raise ValueError('value must be "bar"')

        return v
 """
