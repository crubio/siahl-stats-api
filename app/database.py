from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import sqlitecloud

db_uri = f"{settings.sqlite_uri}{settings.sqlite_db}?apikey={settings.sqlite_api_key}"
conn = sqlitecloud.connect(db_uri)

Base = declarative_base()

# not working with sqlitecloud yet TODO
def get_db():
    db = conn
    try:
        yield db
    finally:
        db.close()

def get_db_url():
    return db_uri