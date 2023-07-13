from pydantic import BaseModel, field_validator


class Search(BaseModel):

    table: str
    fields: list | str
    where: dict | None = {}


"""     @field_validator('where')
    def value_must_equal_bar(cls, v):
        if v != 'bar':
            raise ValueError('value must be "bar"')

        return v
 """
