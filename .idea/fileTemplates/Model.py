from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ${NAME}(Base):
    __tablename__ = ""
    
        @classmethod
    def create${NAME}(cls, db: Session, placeholder):
        try:
            pass
        except SQLAlchemyError as e:
            db.rollback()
            return JSONResponse({"error": str(e.__dict__['orig'])}, status_code=500)

    @classmethod
    def read${NAME}(cls, db: Session, placeholder):
        try:
            pass
        except SQLAlchemyError as e:
            db.rollback()
            return JSONResponse({"error": str(e.__dict__['orig'])}, status_code=500)

    @classmethod
    def read${NAME}(cls, db: Session):
        try:
            pass
        except SQLAlchemyError as e:
            db.rollback()
            return JSONResponse({"error": str(e.__dict__['orig'])}, status_code=500)

    @classmethod
    def update${NAME}(cls, db: Session, placeholder):
        try:
            pass
        except SQLAlchemyError as e:
            db.rollback()
            return JSONResponse({"error": str(e.__dict__['orig'])}, status_code=500)

    @classmethod
    def delete${NAME}(cls, db: Session, placeholder):
        try:
            pass
        except SQLAlchemyError as e:
            db.rollback()
            return JSONResponse({"error": str(e.__dict__['orig'])}, status_code=500)