"""Model Search"""

from pydantic import BaseModel


class Search(BaseModel):
    """Clase Busqueda"""

    query: str
    fields: list | str = "*"
    where: dict | None = None
    order: dict | None = None
    limit: int | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "demo.prueba", "fields": "*"},
            ]
        }
    }


"""     @field_validator('where')
    def value_must_equal_bar(cls, v):
        if v != 'bar':
            raise ValueError('value must be "bar"')

        return v
 """
