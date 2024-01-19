from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from Schemas.SetContatto import setContattoCreate
from Schemas.Contatto import ContattoSchema

Base = declarative_base()


class Contatto(Base):
    __tablename__ = "contatto"

    idIntervistato = Column(Integer, primary_key=True, index=True)
    telefono = Column(String, index=True)
    stato = Column(Integer, default=0)

    @classmethod
    def createContatto(cls, db: Session, contact: setContattoCreate):
        try:
            for telefono in (contact.telAbitazione, contact.telCellulare, contact.telUfficio):
                if telefono and telefono != "":
                    exist = db.query(cls).filter(cls.idIntervistato == contact.idIntervistato, cls.telefono == telefono).first()
                    if not exist:
                        contatto = cls(
                            idIntervistato=contact.idIntervistato,
                            telefono=telefono
                        )
                        db.add(contatto)
                        db.commit()
                else:
                    pass
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def readContatto(cls, db: Session, ids: int):
        try:
            # contatto = db.execute(cls.__table__.select().where(cls.idIntervistato == ids)).fetchall()
            contatto = db.scalars(select(cls).where(cls.idIntervistato == ids)).all()
            return contatto
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def readContatti(cls, db: Session):
        try:
            return db.query(cls).all()
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def updateContatto(cls, db: Session, contact: setContattoCreate):
        try:
            cls.deleteContatto(db, contact.idIntervistato)
            cls.createContatto(db, contact)
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def deleteContatto(cls, db: Session, ids: int):
        try:
            db.query(cls).filter(cls.idIntervistato == ids).delete()
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False
