from pydantic import BaseModel


class IntervistatiTelefonoBaseSchema(BaseModel):
    idIntervistato: int
    Email: str
    nome: str
    cognome: str


class IntervistatiTelefonoCreateSchema(IntervistatiTelefonoBaseSchema):
    pass


class IntervistatiTelefonoSchema(IntervistatiTelefonoBaseSchema):
    telAbitazione: str | None = None
    telCellulare: str | None = None
    telUfficio: str | None = None

    class Config:
        from_attributes = True
