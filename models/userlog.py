from ..database import Base
from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime

class UserLog(Base):
    __tablename__ = 'userlog'
    # Same with 'User' Model
    idx = Column(Integer, autoincrement=True, primary_key=True)
    uid = Column(Integer, nullable=False, unique=True)
    username = Column(VARCHAR(20), nullable=True)
    email = Column(VARCHAR(320), nullable=False)
    is_manager = Column(BOOLEAN, nullable=False)
    punished = Column(BOOLEAN, nullable=False)

    # Modified...
    modified_at = Column(DateTime, nullable=False)
    modified_by = Column(Integer, nullable=False)
    expire_at = Column(DateTime, nullable=False)
    mdtype = Column(VARCHAR(15), nullable=False)

    def __init__(self, uid:int, username:str, email:str, is_manager:bool, punished:bool, modified_by:int, expire_at:datetime, mdtype:str):
        self.uid = uid
        self.username = username
        self.email = email
        self.is_manager = is_manager
        self.punished = punished
        self.modified_at = datetime.now(tz=timezone(timedelta(hours=9)))
        self.modified_by = modified_by
        self.expire_at = expire_at
        self.mdtype = {
            "CREATED":"CREATED",
            "UPDATED":"UPDATED",
            "PUNISHED":"PUNISHED",
            "PUNISH_END":"PUNISH_END",
            "WITHDRAW_SELF":"WITHRAW_SELF",
            "EXPIRED_PUNISH":"EXPIRED_PUNISH"
        }[mdtype]