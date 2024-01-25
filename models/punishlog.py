from ..app import now
from ..database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime

class MissingTgtTypeError(Exception):
    def __init__(self, msg:str):
        self.msg = "Missing Punished target type"

    def __str__(self):
        return self.msg
    
class InvalidTgtTypeError(Exception):
    def __init__(self, msg:str):
        self.msg = "TGTTypes Key Error has raised."

    def __str__(self):
        return self.msg

TGT_TYPES = (
    'ARTICLE',
    'COMMENT',
    'USER'
)

class PunishLog(Base):
    __tablename__ = 'punishlog'
    idx = Column(Integer, autoincrement=True, primary_key=True) # Has Default Value
    src_uid = Column(Integer, nullable=False)
    tgt_id = Column(Integer, nullable=False)
    punish_tgt_typ = Column(VARCHAR(10), nullable=False)
    logged_at = Column(DateTime, nullable=False, default=now()) # Has Default Value
    expire_log_at = Column(DateTime, nullable=False, default=now(90)) # Has Default Value

    def __init__(self, src_uid:int, tgt_id:int, tgt_type:str=None):
        if tgt_type == None:
            raise MissingTgtTypeError
        if tgt_type not in TGT_TYPES:
            raise InvalidTgtTypeError

        self.src_uid = src_uid
        self.tgt_id = tgt_id
        self.punish_tgt_typ = tgt_type