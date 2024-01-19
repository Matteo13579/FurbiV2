from pydantic import BaseModel


class UtenteBaseSchema(BaseModel):
    idIntervistato: int


class UtenteCreateSchema(UtenteBaseSchema):
    pass


class UtenteSchema(UtenteBaseSchema):
    pass

    class Config:
        from_attributes = True
