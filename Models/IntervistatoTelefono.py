from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from Schemas.IntervistatoTelefono import IntervistatiTelefonoCreateSchema

Base = declarative_base()


class IntervistatiTelefono(Base):
    __tablename__ = "IntervistatoTelefono"

    idIntervistato = Column(Integer, primary_key=True, index=True)
    Email = Column(String(200))
    nome = Column(String(40))
    cognome = Column(String(40))
    telAbitazione = Column(String(15))
    telCellulare = Column(String(15))
    telUfficio = Column(String(15))

    @classmethod
    def createIntervistato(cls, db: Session, intervistato: IntervistatiTelefonoCreateSchema):
        try:
            intervistato = cls(
                idIntervistato=intervistato.idIntervistato,
                Email=intervistato.Email,
                nome=intervistato.nome,
                cognome=intervistato.cognome,
                telAbitazione=intervistato.telAbitazione,
                telCellulare=intervistato.telCellulare,
                telUfficio=intervistato.telUfficio
            )
            db.add(intervistato)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def readintervistato(cls, ids: int, db: Session):
        try:
            return db.query(cls).filter(cls.idIntervistato == ids).first()
        except SQLAlchemyError as e:
            return False

    @classmethod
    def readintervistati(cls, db: Session):
        try:
            return db.query(cls).all()
        except SQLAlchemyError as e:
            return False

    @classmethod
    def updateIntervistato(cls, db: Session, intervistato: IntervistatiTelefonoCreateSchema):
        try:
            db.query(cls).filter(cls.idIntervistato == intervistato.idIntervistato).update({
                cls.telAbitazione: intervistato.telAbitazione if not None or not "" else 'NULL',
                cls.telCellulare: intervistato.telCellulare if not None or not "" else 'NULL',
                cls.telUfficio: intervistato.telUfficio if not None or not "" else 'NULL'
            })
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False
