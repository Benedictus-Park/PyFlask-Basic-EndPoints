from .engine import *
from .engine.tools import now
from sqlalchemy.orm import scoped_session

# 유저 검색에 필요한 Key가 누락된 경우 Raise
class InvalidateUserQuery(Exception):
    def __init__(self, msg:str=None):
        self.msg = "This function require 1 parameter at least." if msg != None else msg
    
    def __str__(self):
        return self.msg

class UserDao:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    # Hashed Password가 Parameter로 주어져야 함에 유의.
    def insert_user(self, username:str, email:str, password:str) -> User:
        u = User(username, email, password)
        self.db_session.add(u)
        self.db_session.commit()
        return u

    def get_user(self, uid:int=None, username:str=None, email:str=None, login:bool=False) -> tuple:
        if username == None and email == None:
            raise InvalidateUserQuery()
        elif uid != None:
            return (self.db_session.query(User).filter_by(uid=uid).one_or_none(), False)
        elif username != None:
            return (self.db_session.query(User).filter_by(username=username).one_or_none(), False)
        elif email != None: 
            u = self.db_session.query(User).filter_by(email=email).one_or_none()

            if u != None and login:
                if u.expire_at != None:
                    self.db_session.query(User).filter_by(email=email).update({
                        'expire_at':None
                    })
                    self.db_session.commit()
                    return (u, True)
            return (u, False)
        
    def get_all_users_for_managing(self, only_manager:bool=False) -> tuple:
        users = None
        
        if only_manager:
            users = self.db_session.query(User.uid, User.username, User.email, User.created_at).filter('is_manager' == True and 'expire_at' == None).all()
        else:
            users = self.db_session.query(User.uid, User.username, User.email, User.is_manager, User.created_at, User.punished, User.block_until).filter_by(expire_at=None).all()

        return (users.count(), users)
        
    def update_user(self, uid:int, username:str=None, pwd:str=None, is_manager:bool=None, punished:bool=None, block_until:int=None, expire_after:int=7) -> User:
        u = self.db_session.query(User).filter_by(uid=uid).one_or_none()

        if u == None:
            raise InvalidateUserQuery("Cannot found user by uid.")
            
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
                    "is_manager":False,
                    "punished":True,
                    "block_until":now(expire_after * 2),
                    "expire_at":now(expire_after)
                }
            else:
                params = {
                    "is_manager":False,
                    "punished":True,
                    "block_until":now(block_until)
                }
        else:
            params = {
                "punished":False,
                "expire_at":now(expire_after)
            }
                

        self.db_session.query(User).filter_by(uid=uid).update(params)
        self.db_session.commit()

        u.username = u.username if username == None else username,
        u.is_manager = u.is_manager if is_manager == None else is_manager

        return u
        
    def delete_user(self, uid:int=None):
        self.db_session.query(User).filter_by(uid=uid).delete()
        self.db_session.commit()