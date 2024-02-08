from flask import g
from .engine import *
from sqlalchemy.orm import scoped_session

class Logger:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def user_created(self, u:User):
        self.user_log(u, 0)

    def user_updated(self, u:User):
        self.user_log(u, 1)

    def user_withdraw(self, u:User):
        self.user_log(u, 2)

    def user_punish_block(self, u:User):
        self.user_log(u, 4)

    def user_punish_exp(self, u:User):
        self.user_log(u, 5)

    def user_priv_granted(self, u:User, _by:int=None):
        self.user_log(u, 6, "By manager: " + str(_by))

    def user_priv_revoked(self, u:User, _by:int=None):
        self.user_log(u, 7, "By manager: " + str(_by))

    def user_complete_exp(self, users:tuple):
        userlogs = []
        for user in users:
            userlogs.append(UserLog(user, 8, 'By Robot', 'By Robot'))
        self.db_session.add_all(userlogs)
        self.db_session.commit()

    def authenticate(self, u:User=None, success:bool=None):
        if u == None:
            self.user_log(User.get_dummy(), 10)
        else:
            self.user_log(u, 9 if success else 10)

    def user_log(self, u:User, mdtype:int, etcs:str=None):
        userlog = UserLog(u, mdtype, g.ipv4_addr, etcs)
        self.db_session.add(userlog)
        self.db_session.commit()

    def punish_user(self, src_uid:int, tgt_id:int):
        self.punish_log(src_uid, tgt_id, 0)

    def punish_article(self, src_uid:int, tgt_id:int): #
        self.punish_log(src_uid, tgt_id, 1)

    def punish_comment(self, src_uid:int, tgt_id:int): #
        self.punish_log(src_uid, tgt_id, 2)

    def punish_log(self, src_uid:int, tgt_id:int, mdtype:int):
        punishlog = PunishLog(src_uid, tgt_id, mdtype, g.ipv4_addr)
        self.db_session.add(punishlog)
        self.db_session.commit()