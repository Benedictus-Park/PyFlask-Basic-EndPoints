from .tools import now
from .database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime

class User(Base):
    __tablename__ = "user"
    uid = Column(Integer, autoincrement=True, primary_key=True) # Has Default Value
    username = Column(VARCHAR(20), nullable=False, unique=True)
    email = Column(VARCHAR(320), nullable=False, unique=True)
    pwd = Column(VARCHAR(60), nullable=False)
    is_manager = Column(BOOLEAN, nullable=False, default=False) # Has Default Value
    created_at = Column(DateTime, nullable=False) # Has Default Value
    punished = Column(BOOLEAN, nullable=False, default=False) # Has Default Value
    block_until = Column(DateTime, nullable=True)
    expire_at = Column(DateTime, nullable=True)

    def __init__(self, username:str, email:str, pwd:str, is_manager=False):
        self.username = username
        self.email = email
        self.pwd = pwd
        self.is_manager = is_manager
        self.created_at = now()

    def __repr__(self):
        return f"<DB Table User ({self.uid}, {self.username})>"
    
    def get_dummy():
        u = User("UNKNOWN", "UNKNOWN", "")
        u.uid = 0
        u.created_at = now()

        return u
