from ..database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime

class UserLog(Base):
    __tablename__ = 'userlog'