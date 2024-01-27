import jwt
from flask import g
from config import JWT_SECRET_KEY
from datetime import datetime, timedelta

def jwt_generator(u:any=None, use_g:bool=False, uid:int=None, username:str=None, email:str=None, is_manager:bool=None) -> str:
    payload = None
    if u != None:
        payload = {
            'uid':u.uid,
            'username':u.username,
            'email':u.email,
            'is_manager':u.is_manager,
            'exp':datetime.utcnow() + timedelta(hours=1)
        }
    elif use_g:
        payload = {
            'uid':g.uid,
            'username':g.username,
            'email':g.email,
            'is_manager':g.is_manager,
            'exp':datetime.utcnow() + timedelta(hours=1)
        }
    else:
        if None in (uid, username, email, is_manager):
            raise Exception("This function require (uid, username, email, is_manager).")

        payload = {
            'uid':uid,
            'username':username,
            'email':email,
            'is_manager':is_manager,
            'exp':datetime.utcnow() + timedelta(hours=1)
        }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')