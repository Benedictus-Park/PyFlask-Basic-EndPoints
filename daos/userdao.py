from ..models import *
from sqlalchemy.orm.exc import *
from datetime import datetime, timedelta
from sqlalchemy.orm import scoped_session

# 유저 검색에 필요한 Key가 누락된 경우 Raise
class InvalidateUserQuery(Exception):
    def __init__(self, msg:str):
        self.msg = "This function require 1 parameter at least."
    
    def __str__(self):
        return self.msg

class UserDao:
    def __init__(self, db_session:scoped_session):
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
        
    def update_user(self, uid:int, username:str=None, pwd:str=None, is_manager:bool=None, punished:bool=None, block_until:int=None, expire_after:int=None) -> User:
        if username == None and pwd == None and is_manager == None and punished == None and block_until == None and expire_after == None:
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
                        "blocked_until":datetime.utcnow() + timedelta(days=14),
                        "expire_at":datetime.utcnow() + timedelta(days=7)
                    }
                else:
                    params = {
                        "punished":True,
                        "blocked_until":datetime.utcnow() + timedelta(days=block_until)
                    }
            else:
                params = {
                    "expire_at":datetime.utcnow() + timedelta(days=7)
                }
                

            self.db_session.query(User).filter_by(uid=uid).update(params)
            self.db_session.commit()

            u.username = u.username if username == None else username,
            u.is_manager = u.is_manager if is_manager == None else is_manager

            return u
        
    def delete_user(self, uid:int=None, username:str=None, email:str=None):
        if uid == None and username == None and email == None:
            raise InvalidateUserQuery()
        elif uid != None:
            self.db_session.query(User).filter_by(uid=uid).delete()
        elif username != None:
            self.db_session.query(User).filter_by(username=username).delete()
        elif email != None:
            self.db_session.query(User).filter_by(email=email).delete()
        
        self.db_session.commit()