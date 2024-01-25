from user import User
from ..app import now
from ..database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime

class MissingUserModelError(Exception):
    def __init__(self, msg:str):
        self.msg = "Missing User model. This class only can create with User Model Instance."

    def __str__(self):
        return self.msg

class MissingMdtypeError(Exception):
    def __init__(self, msg:str):
        self.msg = "Missing MDTYPE(Modified Type)"

    def __str__(self):
        return self.msg
    
class InvalidMdtypeError(Exception):
    def __init__(self, msg:str):
        self.msg = "MDType Key Error has raised. Check MDType Parameter."

    def __str__(self):
        return self.msg
    
MDTYPES = (
    'USER_CREATED',
    'USER_UPDATED',
    'USER_WITHDRAW',
    'USER_CANCEL_EXP',
    'PUNISH_BLOCK',
    'PUNISH_EXP',
    'PRIV_GRANT',
    'PRIV_REVOKE'
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
    mdtype = Column(VARCHAR(20), nullable=False)

    def __init__(self, u:User = None, mdtype:str=None):
        if u == None:
            raise MissingUserModelError
        if mdtype == None:
            raise MissingMdtypeError
        elif mdtype not in MDTYPES:
            raise InvalidMdtypeError
        
        self.uid = u.uid
        self.username = u.username
        self.email = u.email
        self.is_manager = u.is_manager
        self.blocked_until = u.blocked_until
        self.mdtype = mdtype