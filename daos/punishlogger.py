from ..models import PunishLog
from sqlalchemy.orm import scoped_session

class PunishLogger:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def punish_user(self, src_uid:int, tgt_id:int):
        self.log(src_uid, tgt_id, 0)

    def punish_article(self, src_uid:int, tgt_id:int):
        self.log(src_uid, tgt_id, 1)

    def punish_comment(self, src_uid:int, tgt_id:int):
        self.log(src_uid, tgt_id, 2)

    def log(self, src_uid:int, tgt_id:int, mdtype:int):
        punishlog = PunishLog(src_uid, tgt_id, mdtype)
        self.db_session.add(punishlog)
        self.db_session.commit()