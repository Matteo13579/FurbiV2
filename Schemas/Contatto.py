from pydantic import BaseModel


class ContattoSchemaBase(BaseModel):
    idIntervistato: int
    telefono: str


class ContattoSchemaCreate(ContattoSchemaBase):
    pass


class ContattoSchema(ContattoSchemaBase):
    stato: int

    class Config:
        from_attributes = True
