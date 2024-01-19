from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from a2wsgi import ASGIMiddleware

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal, engine

from Models.IntervistatoTelefono import IntervistatiTelefono as IntervistatoTelefonoModel, Base as ITBase
from Models.Contatto import Contatto as ContattoModel, Base as CBase
from Models.Utente import Utente as UtenteModel, Base as UBase
from Models.Ban import Ban as BanModel, Base as BBase
from Models.Family import Famiglia as FamigliaModel, Base as FBase

from Schemas.IntervistatoTelefono import IntervistatiTelefonoSchema
from Schemas.SetContatto import setContattoCreate
from Schemas.Contatto import ContattoSchema
from Schemas.Utente import UtenteSchema
from Schemas.Ban import BanSchema
from Schemas.Family import FamilySchema

ITBase.metadata.create_all(bind=engine)
CBase.metadata.create_all(bind=engine)
UBase.metadata.create_all(bind=engine)
BBase.metadata.create_all(bind=engine)
FBase.metadata.create_all(bind=engine)

with open("description.md", "r") as description:
    description = description.read()

app = FastAPI(
    title="FurbiOC V2",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Matteo Paone",
        "email": "matteo@testpoint.it",
    },
    description=description
)



templates = Jinja2Templates(directory="templates")

wsgi_app = ASGIMiddleware(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# region Root route
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# endregion


# region Intervistato
# region Intervistato per ID
@app.get("/IntervistatoById/", response_model=IntervistatiTelefonoSchema, tags=["Intervistati"])
def getintervistatobyid(userId: int, db: Session = Depends(get_db)):
    try:
        intervistato = IntervistatoTelefonoModel.readintervistato(userId, db)
        if intervistato:
            return intervistato
        else:
            return JSONResponse(status_code=400, content={"error": "Interviewer not found"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})


# endregion


# region Intervistati
@app.get("/Intervistati/", tags=["Intervistati"])
def getintervistati(db: Session = Depends(get_db)):
    try:
        Intervistati = IntervistatoTelefonoModel.readintervistati(db)
        totale = Intervistati.__len__()

        result = {
            "totale": totale,
            "intervistati": Intervistati
        }

        return result
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})


# endregion


# region Create Intervistato
@app.post("/setIntervistato/", tags=["Intervistati"])
def addIntervistato(intervistato: IntervistatiTelefonoSchema, db: Session = Depends(get_db)):
    try:
        db_user = IntervistatoTelefonoModel.readintervistato(intervistato.idIntervistato, db)
        if db_user:
            return JSONResponse(status_code=400, content={"error": "User already registered"})
        else:
            check = IntervistatoTelefonoModel.createIntervistato(db, intervistato)
            if check:
                ContattoModel.createContatto(db, setContattoCreate(
                    idIntervistato=intervistato.idIntervistato,
                    telAbitazione=intervistato.telAbitazione,
                    telCellulare=intervistato.telCellulare,
                    telUfficio=intervistato.telUfficio)
                                             )
                return JSONResponse(status_code=200, content={"Success": "User registered"})
            else:
                return JSONResponse(status_code=400, content={"error": "User not registered"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})


# endregion


# region Update Intervistato
@app.put("/updateIntervistato/", tags=["Intervistati"])
def changeIntervistato(intervistato: IntervistatiTelefonoSchema, db: Session = Depends(get_db)):
    try:
        db_user = IntervistatoTelefonoModel.readintervistato(intervistato.idIntervistato, db)
        if not db_user:
            return JSONResponse(status_code=400, content={"error": "User not found"})
        else:
            check = IntervistatoTelefonoModel.updateIntervistato(db, intervistato)
            if check:
                ContattoModel.updateContatto(db, setContattoCreate(
                    idIntervistato=intervistato.idIntervistato,
                    telAbitazione=intervistato.telAbitazione,
                    telCellulare=intervistato.telCellulare,
                    telUfficio=intervistato.telUfficio)
                                             )
                return JSONResponse(status_code=200, content={"Success": "User updated"})
            else:
                return JSONResponse(status_code=400, content={"error": "User not update"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})


# endregion
# endregion


# region Utente
# region Utente per ID
@app.get("/UtenteById/", response_model=UtenteSchema, tags=["Utenti"])
def getutentebyid(userId: int, db: Session = Depends(get_db)):
    try:
        utente = UtenteModel.readUtente(db, userId)
        if utente:
            return utente
        else:
            return JSONResponse(status_code=400, content={"error": "User not found"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion


# region Utenti
@app.get("/Utenti/", tags=["Utenti"])
def getutenti(db: Session = Depends(get_db)):
    try:
        Utenti = UtenteModel.readUtenti(db)
        totale = Utenti.__len__()

        result = {
            "totale": totale,
            "utenti": Utenti
        }

        return result
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})


# endregion


# region Create Utente
@app.post("/setUtente/", tags=["Utenti"])
def addUtente(utenti: list[UtenteSchema], db: Session = Depends(get_db)):
    try:
        for utente in utenti:
            db_user = UtenteModel.readUtente(db, utente.idIntervistato)
            if db_user:
                return JSONResponse(status_code=400, content={"error": "User already registered"})
            else:
                check = UtenteModel.createUtente(db, utente)
                if check:
                    return JSONResponse(status_code=200, content={"Success": "User registered"})
                else:
                    return JSONResponse(status_code=400, content={"error": "User not registered"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion
# endregion


# region Contatto
# region Contatto per ID
@app.get("/ContattoById/", response_model=list[ContattoSchema], tags=["Contatti"])
def getcontattobyid(userId: int, db: Session = Depends(get_db)):
    try:
        contatto = ContattoModel.readContatto(db, userId)
        if contatto:
            return contatto
        else:
            return JSONResponse(status_code=400, content={"error": "User not found"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion


# region Contatti
@app.get("/Contatti/", tags=["Contatti"])
def getcontatti(db: Session = Depends(get_db)):
    try:
        Contatti = ContattoModel.readContatti(db)
        totale = Contatti.__len__()

        result = {
            "totale": totale,
            "contatti": Contatti
        }

        return result
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion


# region Create Contatto
@app.post("/setContatto/", tags=["Contatti"])
def addContatto(contatto: setContattoCreate, db: Session = Depends(get_db)):
    try:
        db_user = ContattoModel.readContatto(db, contatto.idIntervistato)
        if db_user:
            return JSONResponse(status_code=400, content={"error": "Contact already registered"})
        else:
            check = ContattoModel.createContatto(db, contatto)
            if check:
                return JSONResponse(status_code=200, content={"Success": "Contact registered"})
            else:
                return JSONResponse(status_code=400, content={"error": "Contact not registered"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion


# region Update Contatto
@app.put("/updateContatto/", tags=["Contatti"])
def changeContatto(contatto: setContattoCreate, db: Session = Depends(get_db)):
    try:
        db_user = ContattoModel.readContatto(db, contatto.idIntervistato)
        if not db_user:
            return JSONResponse(status_code=400, content={"error": "Contact not found"})
        else:
            check = ContattoModel.updateContatto(db, contatto)
            if check:
                return JSONResponse(status_code=200, content={"Success": "Contact updated"})
            else:
                return JSONResponse(status_code=400, content={"error": "Contact not update"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion
# endregion


# region Ban
# region Ban per ID
@app.get("/getBan/", tags=["Ban"])
def getban(userId: int, db: Session = Depends(get_db)):
    try:
        return BanModel.readBan(db, userId)
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion


# region Bans
@app.get("/getBans/", tags=["Ban"])
def getbans(db: Session = Depends(get_db)):
    try:
        bans = BanModel.readBans(db)
        totale = bans.__len__()

        result = {
            "totale": totale,
            "bans": bans
        }
        return result
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion


# region Create Ban
@app.post("/setBan/", tags=["Ban"])
def addBan(bans: list[BanSchema], db: Session = Depends(get_db)):
    try:
        counter = 0
        for ban in bans:
            db_user = BanModel.readBan(db, ban)
            if db_user:
                return JSONResponse(status_code=400, content={"error": "User already banned"})
            else:
                check = BanModel.createBan(db, ban)
                if check:
                    counter += 1
                else:
                    return JSONResponse(status_code=400, content={"error": "User not banned"})
        if counter == 1:
            return JSONResponse(status_code=200, content={"Success": "User banned"})
        elif counter > 1:
            return JSONResponse(status_code=200, content={"Success": "Users banned"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion
# endregion


# region Family
# region Family per FamID
@app.get("/getFamilyByFamID/", tags=["Family"])
def getfamilybyfamid(famId: int, db: Session = Depends(get_db)):
    try:
        return FamigliaModel.readFamilyByFamId(db, famId)
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion
    

# region Family per UserID
@app.get("/getFamilyByUserID/", tags=["Family"])
def getfamilybyuserid(userId: int, db: Session = Depends(get_db)):
    try:
        return FamigliaModel.readFamilyByUserId(db, userId)
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion


# region Families
@app.get("/getFamilies/", tags=["Family"])
def getfamilies(db: Session = Depends(get_db)):
    try:
        families = FamigliaModel.readFamilies(db)
        totaleFamiglie = FamigliaModel.readMaxID(db)
        totale = families.__len__()

        result = {
            "totale": totale,
            "totaleFamiglie": totaleFamiglie,
            "families": families
        }
        return result
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion


# region Create Family
@app.post("/setFamily/", tags=["Family"])
def addFamily(families: list[FamilySchema], db: Session = Depends(get_db)):
    try:
        familyID = FamigliaModel.readMaxID(db)
        
        if familyID is None:
            familyID = 0

        for family in families:
            db_user = FamigliaModel.readFamilyByUserId(db, family.idIntervistato)
            if db_user:
                return JSONResponse(status_code=400, content={"error": "User already in family"})
            else:
                check = FamigliaModel.createFamiglia(db, family, familyID)
                if check:
                    continue
                else:
                    return JSONResponse(status_code=400, content={"error": "Family not registered"})
        return JSONResponse(status_code=200, content={"Success": "Family registered"})
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"Database Error: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unknown Error: {str(e)}"})
# endregion
# endregion