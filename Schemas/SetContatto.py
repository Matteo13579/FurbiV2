from pydantic import BaseModel


class setContattoBase(BaseModel):
    idIntervistato: int
    telAbitazione: str | None = None
    telCellulare: str | None = None
    telUfficio: str | None = None


class setContattoCreate(setContattoBase):
    pass


class setContatto(setContattoBase):
    pass

    class Config:
        from_attributes = True
