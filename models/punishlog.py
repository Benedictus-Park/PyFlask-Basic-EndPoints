from ..database import Base
from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DateTime

class PunishLog(Base):
    __tablename__ = 'punishlog'
    idx = Column(Integer, autoincrement=True, primary_key=True)
    src_uid = Column(Integer, nullable=False)
    tgt_id = Column(Integer, nullable=False)
    pntype = Column(VARCHAR(20), nullable=False)
    logged_at = Column(DateTime, nullable=False)
    expire_at = Column(DateTime, nullable=False)

    def __init__(self):
        pass