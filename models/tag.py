import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator

class Tag(BaseModel):
    name: str = Field(...)
    datetime: datetime.datetime
    tipo: Literal["int", "bool"]
    value:  int | bool


    @validator("tipo")
    def tipo_valido(cls, v):
        if v not in ["int", "bool"]:
            raise ValueError("Tipo inválido")
        return v

    @validator("value")
    def valor_compativel(cls, v, values):
        tipo = values.get("tipo")
        if tipo == "int" and not isinstance(v, int):
            raise TypeError("Valor deve ser int")
        elif tipo == "bool" and not isinstance(v, bool):
            raise TypeError("Valor deve ser bool")
        return v

class TagUpdate(Tag):
    updated: bool
    station: str
    user: str