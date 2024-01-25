from ..models import *
from sqlalchemy.orm import scoped_session

class Logger:
    def user_created(self, u:User):
        self.user_log(u, 0)

    def user_updated(self, u:User):
        self.user_log(u, 1)

    def user_withdraw(self, u:User): #
        self.user_log(u, 2)

    def user_cancel_exp(self, u:User): #
        self.user_log(u, 3)

    def user_punish_block(self, u:User): #
        self.user_log(u, 4)

    def user_punish_exp(self, u:User): #
        self.user_log(u, 5)

    def user_priv_granted(self, u:User): #
        self.user_log(u, 6)

    def user_priv_revoked(self, u:User): #
        self.user_log(u, 7)

    def user_complete_exp(self, u:User): #
        self.user_log(u, 8)

    def user_log(self, u:User, mdtype:int):
        userlog = UserLog(u, mdtype)
        self.db_session.add(userlog)
        self.db_session.commit()

    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def punish_user(self, src_uid:int, tgt_id:int):
        self.punish_log(src_uid, tgt_id, 0)

    def punish_article(self, src_uid:int, tgt_id:int): #
        self.punish_log(src_uid, tgt_id, 1)

    def punish_comment(self, src_uid:int, tgt_id:int): #
        self.punish_log(src_uid, tgt_id, 2)

    def punish_log(self, src_uid:int, tgt_id:int, mdtype:int):
        punishlog = PunishLog(src_uid, tgt_id, mdtype)
        self.db_session.add(punishlog)
        self.db_session.commit()