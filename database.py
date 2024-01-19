from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

driver = 'ODBC Driver 18 for SQL Server'
user = "wata"
password = '7FK51BtPR6QVrqmEdADm'
host = "wata.database.windows.net"
schema = "furbetti"

conn = f"mssql+pyodbc://{user}:{password}@{host}/{schema}?driver={driver}"

engine = create_engine(conn)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)