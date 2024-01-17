import jwt
from functools import wraps
from flask_cors import CORS
from datetime import datetime, timedelta
from flask import Flask, request, g, Response

# 사용자 정의 모듈/패키지
from daos import *
from services import *
from database import db_session
from config import JWT_SECRET_KEY

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('authorization')

        if access_token is None:
            return Response(status=400)
        else:
            try:
                payload = jwt.decode(access_token, JWT_SECRET_KEY, 'HS256')
            except Exception:
                return Response(status=401)
            
            g.uid = payload['uid']
            g.username = payload['username']
            g.email = payload['email']
            g.is_manager = payload['is_manager']

        return f(*args, **kwargs)
    return wrapper

def priv_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.is_manager == False:
            return Response(status=401)
        return f(*args, **kwargs)
    return wrapper

def jwt_generator(uid:int, username:str, email:str, is_manager:bool) -> str:
    # 기본 Token 유효 시간: 1h
    return jwt.encode({
        'uid':uid,
        'username':username,
        'email':email,
        'is_manager':is_manager,
        'exp':datetime.utcnow() + timedelta(hours=1)
    }, JWT_SECRET_KEY, algorithm='HS256')

app = Flask(__name__)
CORS(app)

services = dict()
services['User'] = UserService(UserDao(db_session), jwt_generator)

# 회원가입 처리 Endpoint
@app.route("/registration", methods=["POST"])
def registration():
    payload = request.get_json()
    
    try:
        username = payload['username']
        email = payload['email']
        password = payload['password']
    except KeyError:
        return Response(status=400)

    return services['User'].registration_service(username, email, password)

# 로그인 처리 Endpoint
@app.route("/authenticate", methods=["POST"])
def authenticate():
    payload = request.get_json()
    keys = payload.keys()

    if 'email' not in keys or 'password' not in keys:
        return Response(status=400)
    
    email = payload['email']
    password = payload['password']

    return services['User'].authentication_service(email, password)

# 회원정보(유저명, 패스워드) 업데이트, 권한 업데이트는 지원하지 않음.
@login_required
@app.route("/update-userinfo", methods=["POST"])
def update_userinfo():
    payload = request.get_json()

    if 'cur_password' not in keys:
        return Response(status=400)

    keys = payload.keys()
    update_info = {
        "uid":g.uid,
        "username":None,
        "cur_password":payload['cur_password'],
        "new_password":None,
        "is_manager":None,
        "force":True if g.is_manager else False
    }

    if 'username' in keys:
        update_info['username'] = payload['username']
    if 'new_password' in keys:
        update_info['new_password'] = payload['new_password']

    return services['User'].userinfo_update_service(**update_info)

# 회원 권한 정보 업데이트
@login_required
@priv_required
@app.route("/update-user-privilege", methods=["POST"])
def update_user_privilege():
    payload = request.get_json()
    keys = payload.keys()

    if 'is_manager' not in keys or 'tgt_uid' not in keys:
        return Response(status=400)
    
    update_info = {
        "uid":payload['tgt_uid'],
        "username":None,
        "cur_password":None,
        "new_password":None,
        "is_manager":payload['is_manager']
    }

    return services['User'].userinfo_update_service(**update_info, access_token=jwt_generator(
        g.uid,
        g.username,
        g.email,
        g.is_manager
    ))

# 회원 제재
@login_required
@priv_required
@app.route("/punish-user", methods=["POST"])
def punish_user():
    payload = request.get_json()
    keys = payload.keys()

    if 'tgt_uid' not in keys:
        return Response(status=400)
    
    if 'block_until' in keys:
        return services['User'].punish_user_service(tgt_uid=payload['tgt_uid'], access_token=jwt_generator(
            g.uid,
            g.username,
            g.email,
            g.is_manager
        ))
    else:
        return services['User'].punish_user_service(tgt_uid=payload['tgt_uid'], block_until=payload['block_until'], access_token=jwt_generator(
            g.uid,
            g.username,
            g.email,
            g.is_manager
        ))