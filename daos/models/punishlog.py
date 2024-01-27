from .tools import now
from .database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime

TGT_TYPES = (
    'user',
    'article',
    'comment'
)

class PunishLog(Base):
    __tablename__ = 'punishlog'
    idx = Column(Integer, autoincrement=True, primary_key=True) # Has Default Value
    src_uid = Column(Integer, nullable=False)
    tgt_id = Column(Integer, nullable=False)
    punish_tgt_typ = Column(VARCHAR(7), nullable=False)
    logged_at = Column(DateTime, nullable=False, default=now()) # Has Default Value
    expire_log_at = Column(DateTime, nullable=False, default=now(90)) # Has Default Value
    ipv4_addr = Column(VARCHAR(15), nullable=False)

    def __init__(self, src_uid:int, tgt_id:int, tgt_type:int, ipv4_addr:str):
        self.src_uid = src_uid
        self.tgt_id = tgt_id
        self.punish_tgt_typ = TGT_TYPES[tgt_type]
        self.ipv4_addr = ipv4_addr