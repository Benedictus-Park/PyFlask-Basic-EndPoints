from sqlalchemy.dialects import mysql
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DB_URL

engine = create_engine(DB_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.metadata = MetaData()
Base.query = db_session.query_property()

def init_database():
    from . import User, UserLog, PunishLog
    Base.metadata.create_all(engine)