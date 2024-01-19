from sqlalchemy import Integer, Column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, Session
from starlette.responses import JSONResponse

from Schemas.Utente import UtenteCreateSchema

Base = declarative_base()


class Utente(Base):
    __tablename__ = "Utenti"

    idIntervistato = Column(Integer, primary_key=True, index=True)

    @classmethod
    def createUtente(cls, db: Session, utente: UtenteCreateSchema):
        try:
            utente = cls(
                idIntervistato=utente.idIntervistato
            )
            db.add(utente)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()

            return False

    @classmethod
    def readUtente(cls, db: Session, idUtente: int):
        try:
            return db.query(cls).filter(cls.idIntervistato == idUtente).first()
        except SQLAlchemyError as e:
            return False

    @classmethod
    def readUtenti(cls, db: Session):
        try:
            return db.query(cls).all()
        except SQLAlchemyError as e:
            return False

    @classmethod
    def updateUtente(cls, db: Session, utente: UtenteCreateSchema):
        try:
            db.query(cls).filter(cls.idIntervistato == utente.idIntervistato).update({
                cls.idIntervistato: utente.idIntervistato
            })
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def deleteUtente(cls, db: Session, idUtente: int):
        try:
            db.query(cls).filter(cls.idIntervistato == idUtente).delete()
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False
