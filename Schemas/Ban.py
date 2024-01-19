from pydantic import BaseModel


class BanSchemaBase(BaseModel):
    idIntervistato: int


class BanSchemaCreate(BanSchemaBase):
    pass


class BanSchema(BanSchemaBase):
    pass

    class Config:
        from_attributes = True
