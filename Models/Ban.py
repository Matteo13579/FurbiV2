from sqlalchemy import Integer, Column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, Session

from Schemas.Ban import BanSchemaCreate

Base = declarative_base()


class Ban(Base):
    __tablename__ = "bannati"

    idIntervistato = Column(Integer, primary_key=True, index=True)

    @classmethod
    def createBan(cls, db: Session, ban: BanSchemaCreate):
        try:
            banUser = cls(idIntervistato=ban.idIntervistato)
            db.add(banUser)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def readBan(cls, db: Session, ids):
        try:
            return db.query(cls).filter(cls.idIntervistato == ids).first()
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def readBans(cls, db: Session):
        try:
            return db.query(cls).all()
        except SQLAlchemyError as e:
            db.rollback()
            return False

    @classmethod
    def deleteBan(cls, db: Session, ids):
        try:
            db.query(cls).filter(cls.idIntervistato == ids).delete()
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False
