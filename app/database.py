from typing import Union, Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_server = os.environ.get("HOST_SERVER")
db_name = os.environ.get("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = "postgresql://{username}:{password}@{server}/{database}".format(username=db_username, password=db_password, server=db_server, database=db_name)
engine = create_engine(SQLALCHEMY_DATABASE_URL,)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
