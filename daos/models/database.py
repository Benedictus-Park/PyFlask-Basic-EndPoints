from config import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(DB_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_database():
    from daos.models import User, UserLog, PunishLog
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_database()