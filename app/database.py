from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

###
# DB Setup
###
SQL_DB_URL = settings.db_url
engine = create_engine(SQL_DB_URL)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    FastAPI db dependency

    Yields:
        sessionmaker: DB session
    """
    db = db_session()
    try:
        yield db
    finally:
        db.close()
