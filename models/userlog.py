from user import User
from ..app import now
from ..database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime
    
MDTYPES = (
    'USER_CREATED',
    'USER_UPDATED',
    'USER_WITHDRAW',
    'USER_CANCEL_EXP',
    'PUNISH_BLOCK',
    'PUNISH_EXP',
    'PRIV_GRANT',
    'PRIV_REVOKE',
    "COMPLETE_EXP"
)

class UserLog(Base):
    __tablename__ = 'user'
    idx = Column(Integer, autoincrement=True, primary_key=True) # Has Default Value
    uid = Column(Integer, nullable=False)
    username = Column(VARCHAR(20), nullable=False)
    email = Column(VARCHAR(320), nullable=False)
    is_manager = Column(BOOLEAN, nullable=False)
    modified_at = Column(DateTime, nullable=False, default=now()) # Has Default Value
    blocked_until = Column(DateTime, nullable=True)
    expire_log_at = Column(DateTime, nullable=False, default=now(90)) # Has Default Value
    mdtype = Column(VARCHAR(15), nullable=False)

    def __init__(self, u:User, mdtype:int):
        self.uid = u.uid
        self.username = u.username
        self.email = u.email
        self.is_manager = u.is_manager
        self.blocked_until = u.blocked_until
        self.mdtype = MDTYPES[mdtype]