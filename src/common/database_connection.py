from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import CONF

Base = declarative_base()
database_config = CONF["Database"]
engine = create_engine(
    url=("mysql+mysqldb://"+ database_config.get("user") + ":" + database_config.get("password") + "@"+database_config.get("host") + "/" + database_config.get("db_name")),
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=28000
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

