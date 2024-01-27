import time
from ..app import now
from ..models import *
from logger import Logger
from threading import Thread
from sqlalchemy.orm import scoped_session

def safe_join(tr:Thread):
    tr.join()

def _manage_user(logger:Logger, db_session:scoped_session):
    users = db_session.query(User).filter('expire_at' < now() and 'expire_at' != None).all()
    logger.user_complete_exp(tuple(users))
    db_session.query(User).filter('expire_at' < now() and 'expire_at' != None).delete()

def _manage_userlog(db_session:scoped_session):
    db_session.query(UserLog).filter('expire_log_at' < now()).delete()

def _manage_punishlog(db_session:scoped_session):
    db_session.query(PunishLog).filter('expire_log_at' < now()).delete()

def job(logger:Logger, db_session:scoped_session):
    while True:
        _manage_user(logger, db_session)
        _manage_userlog(db_session)
        _manage_punishlog(db_session)
        db_session.commit()
        time.sleep(300)

class Robot:
    def __init__(self, logger:Logger, db_session:scoped_session):
        self.tr:Thread = None
        self.logger = logger
        self.db_session = db_session

    def start(self):
        if self.tr != None:
            if not self.tr.is_alive():
                self.tr = None
        else:
            self.tr = Thread(target=job, args=(self.logger, self.db_session))
            self.tr.start()
    
    def stop(self):
        if self.tr != None:
            if self.tr.is_alive():
                Thread(target=safe_join, args=(self.tr)).start()
            self.tr = None
