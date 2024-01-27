import time
from .engine import *
from .logger import Logger
from threading import Thread
from .engine.tools import now
from sqlalchemy.orm import scoped_session

def safe_join(tr:Thread):
    tr.join()

def _manage_user(logger:Logger, db_session:scoped_session):
    delete_tgt = []
    users = db_session.query(User).filter('expire_at' != None).all()

    for user in users:
        if user.expire_at < now():
            delete_tgt.append(user)
            db_session.query(User).filter(uid=user.uid).delete()
    logger.user_complete_exp(tuple(delete_tgt))

def _manage_userlog(db_session:scoped_session):
    logs = db_session.query(UserLog).all()

    for log in logs:
        if log.expire_log_at < now():
            db_session.query(UserLog).filter_by(idx=log.idx)

def _manage_punishlog(db_session:scoped_session):
    logs = db_session.query(PunishLog).all()

    for log in logs:
        if log.expire_log_at < now():
            db_session.query(PunishLog).filter_by(idx=log.idx)

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
