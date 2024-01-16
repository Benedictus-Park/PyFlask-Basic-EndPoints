from ..database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN;

class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(VARCHAR(20), nullable=False, unique=True)
    email = Column(VARCHAR(320), nullable=False, unique=True)
    pwd = Column(VARCHAR(60), nullable=False)
    is_manager = Column(BOOLEAN, nullable=False, default=False)

    def __init__(self, username:str, email:str, pwd:str, is_manager=False):
        self.username = username
        self.email = email
        self.pwd = pwd
        self.is_manager = is_manager

    def __repr__(self):
        return f"<DB Table User ({self.uid}, {self.username})>"