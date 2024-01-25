from ..app import now
from ..database import Base
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime

class PunishLog(Base):
    __tablename__ = 'punishlog'
    idx = Column(Integer, autoincrement=True, primary_key=True)
    src_uid = Column(Integer, nullable=False)
    tgt_id = Column(Integer, nullable=False)
    punish_tgt_typ = Column(VARCHAR(20), nullable=False)
    logged_at = Column(DateTime, nullable=False, default=now()) # Has Default Value
    expire_log_at = Column(DateTime, nullable=False, default=now(90)) # Has Default Value

    def __init__(self):
        pass