from ..models import User, UserLog
from sqlalchemy.orm import scoped_session

class UserLogger:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def user_created(self, u:User):
        self.log(u, 0)

    def user_updated(self, u:User):
        self.log(u, 1)

    def user_withdraw(self, u:User):
        self.log(u, 2)

    def user_cancel_exp(self, u:User):
        self.log(u, 3)

    def user_punish_block(self, u:User):
        self.log(u, 4)

    def user_punish_exp(self, u:User):
        self.log(u, 5)

    def user_priv_granted(self, u:User):
        self.log(u, 6)

    def user_priv_revoked(self, u:User):
        self.log(u, 7)

    def user_complete_exp(self, u:User):
        self.log(u, 8)

    def log(self, u:User, mdtype:int):
        userlog = UserLog(u, mdtype)
        self.db_session.add(userlog)
        self.db_session.commit()
