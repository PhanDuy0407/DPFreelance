from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import CONF

Base = declarative_base()
database_config = CONF["Database"]
engine = create_engine("mysql+mysqldb://"+ database_config.get("user") + ":" + database_config.get("password") + "@"+database_config.get("host") + "/" + database_config.get("db_name"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

