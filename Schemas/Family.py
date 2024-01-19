from pydantic import BaseModel


class FamilyBaseSchema(BaseModel):
    idIntervistato: int


class FamilyCreateSchema(FamilyBaseSchema):
    pass


class FamilySchema(FamilyBaseSchema):
    idFamiglia: int | None = None

    class Config:
        from_attributes = True