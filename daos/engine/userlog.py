from .user import User
from .tools import now
from .database import Base
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
    "COMPLETE_EXP",
    "LOGIN_OK",
    "LOGIN_FAIL"
)

class UserLog(Base):
    __tablename__ = "userlog"
    idx = Column(Integer, autoincrement=True, primary_key=True) # Has Default Value
    uid = Column(Integer, nullable=False)
    username = Column(VARCHAR(20), nullable=False)
    email = Column(VARCHAR(320), nullable=False)
    is_manager = Column(BOOLEAN, nullable=False)
    modified_at = Column(DateTime, nullable=False) # Has Default Value
    block_until = Column(DateTime, nullable=True)
    expire_log_at = Column(DateTime, nullable=False) # Has Default Value
    mdtype = Column(VARCHAR(15), nullable=False)
    ipv4_addr = Column(VARCHAR(15), nullable=False)
    etcs = Column(VARCHAR(20), nullable=True)

    def __init__(self, u:User=None, mdtype:int=None, ipv4_addr:str=None, etcs:str=None):
        if u != None:
            self.uid = u.uid
            self.username = u.username
            self.email = u.email
            self.is_manager = u.is_manager
            self.block_until = u.block_until
            self.mdtype = MDTYPES[mdtype]
        else:
            self.uid = -1
            self.username = "UNKNOWN"
            self.email = "UNKNOWN"
            self.is_manager = False
            self.block_until = None
            self.mdtype = MDTYPES[10]

        self.modified_at = now()
        self.expire_log_at = now(90)
        self.ipv4_addr = ipv4_addr
        self.etcs = etcs
        
