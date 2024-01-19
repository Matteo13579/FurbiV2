from sqlalchemy import Column, Integer, select, func
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError

from Schemas.Family import FamilyCreateSchema

Base = declarative_base()


class Famiglia(Base):
    __tablename__ = "famiglia"

    idIntervistato = Column(Integer, primary_key=True, index=True)
    idFamiglia = Column(Integer, index=True)

    @classmethod
    def createFamiglia(cls, db: Session, famiglia: FamilyCreateSchema, idFam: int):
        try:
            familyUser = cls(
                idIntervistato=famiglia.idIntervistato,
                idFamiglia=idFam+1
            )
            db.add(familyUser)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False
        
    @classmethod
    def readFamilyByFamId(cls, db: Session, famId: int):
        try:
            return db.query(cls).filter(cls.idFamiglia == famId).all() if not None else None
        except SQLAlchemyError as e:
            return False
        
    @classmethod
    def readFamilyId(cls, db: Session, ids: int):
        try:
            return db.query(cls).filter(cls.idIntervistato == ids).first() if not None else None
        except SQLAlchemyError as e:
            return False

    @classmethod
    def readFamilyByUserId(cls, db: Session, ids: int):
        try:
            familyId = cls.readFamilyId(db, ids)
            if not familyId:
                return None
            else:
                idFam = familyId.idFamiglia
                return db.query(cls).filter(cls.idFamiglia == idFam).all()
        except SQLAlchemyError as e:
            return False
        
    @classmethod
    def readFamilies(cls, db: Session):
        try:
            return db.query(cls).all()
        except SQLAlchemyError as e:
            return False
        
    @classmethod
    def readMaxID(cls, db: Session):
        try:
            return db.scalar(select(func.max(cls.idFamiglia)))
        except SQLAlchemyError as e:
            return False