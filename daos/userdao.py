from ..models import *
from sqlalchemy.orm.exc import *
from sqlalchemy.orm import scoped_session
from datetime import datetime, timedelta, timezone

# 유저 검색에 필요한 Key가 누락된 경우 Raise
class InvalidateUserQuery(Exception):
    def __init__(self, msg:str):
        self.msg = "This function require 1 parameter at least."
    
    def __str__(self):
        return self.msg

class UserDao:
    def __init__(self, db_session:scoped_session):
        self.KST = timezone(timedelta(hours=9))
        self.db_session = db_session

    # Hashed Password가 Parameter로 주어져야 함에 유의.
    def insert_user(self, username:str, email:str, password:str):
        u = User(username, email, password)
        self.db_session.add(u)
        self.db_session.commit()

    def get_user(self, uid:int=None, username:str=None, email:str=None) -> User:
        if username == None and email == None:
            raise InvalidateUserQuery()
        elif uid != None:
            return self.db_session.query(User).filter_by(uid=uid).one_or_none()
        elif username != None:
            return self.db_session.query(User).filter_by(username=username).one_or_none()
        elif email != None:
            return self.db_session.query(User).filter_by(email=email).one_or_none()
        
    def get_all_users_for_managing(self, only_manager:bool=False) -> tuple:
        users = None
        
        if only_manager:
            users = self.db_session.query(User.uid, User.username, User.email, User.created_at).filter_by(is_manager=True).all()
        else:
            users = self.db_session.query(User.uid, User.username, User.email, User.is_manager, User.created_at, User.punished, User.blocked_until).all()

        return (users.count(), users)
        
    def update_user(self, uid:int, username:str=None, pwd:str=None, is_manager:bool=None, punished:bool=None, block_until:int=None, expire_after:int=None) -> User:
        if None in (username, pwd, is_manager, punished, block_until, expire_after):
            raise InvalidateUserQuery()
        else:
            u = self.db_session.query(User).filter_by(uid=uid).one_or_none()

            if u == None:
                return None
            
            params = dict()
            
            if punished == None:
                params = {
                        "username":u.username if username == None else username,
                        "pwd":u.pwd if pwd == None else pwd,
                        "is_manager":u.is_manager if is_manager == None else is_manager
                    }
            elif punished:
                if block_until == None:
                    params = {
                        "punished":True,
                        "blocked_until":datetime.now(tz=self.KST) + timedelta(days=14),
                        "expire_at":datetime.now(tz=self.KST) + timedelta(days=7)
                    }
                else:
                    params = {
                        "punished":True,
                        "blocked_until":datetime.now(tz=self.KST) + timedelta(days=block_until)
                    }
            else:
                params = {
                    "expire_at":datetime.now(tz=self.KST) + timedelta(days=7)
                }
                

            self.db_session.query(User).filter_by(uid=uid).update(params)
            self.db_session.commit()

            u.username = u.username if username == None else username,
            u.is_manager = u.is_manager if is_manager == None else is_manager

            return u
        
    def delete_user(self, uid:int=None):
        self.db_session.query(User).filter_by(uid=uid).delete()
        self.db_session.commit()