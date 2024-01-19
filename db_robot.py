import time
from threading import Thread
from datetime import datetime
from sqlalchemy.orm import scoped_session

from models import *

class DB_Robot:
    def __init__(self, secs:int, db_session:scoped_session):
        self.session = db_session
        self.secs = secs
        self.ticker = None

    def start(self):
        if self.ticker != None:
            if self.ticker.is_alive():
                return
        # Add functions...

    def stop(self):
        Thread(target=self.destroy_thread_safe, args=(self.ticker))
        self.ticker = None

def destroy_thread_safe(thread:Thread):
    thread.join()

def jobs(secs:int, session:scoped_session):
    def _manage_expired_users(session:scoped_session):
        pass

    def _manage_punishment(session:scoped_session):
        pass

    def _manage_expired_logs(session:scoped_session):
        pass

    while True:
        _manage_expired_users(session)
        _manage_punishment(session)
        _manage_expired_logs(session)
        time.sleep(secs=secs)