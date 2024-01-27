import os, sys, jwt
from daos import *
from services import *
from functools import wraps
from flask_cors import CORS
from config import JWT_SECRET_KEY
from services.tools import jwt_generator
from flask import Flask, request, g, Response
from daos.engine.database import init_database, db_session

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

sys.path.insert(1, os.path.abspath('.'))

app = Flask(__name__)
CORS(app)

logger = Logger(db_session)

services = dict()
services['User'] = UserService(UserDao(db_session), logger, jwt_generator)
services['Punish'] = PunishService(UserDao(db_session), logger, jwt_generator)

db_robot = Robot(logger, db_session)
db_robot.start()

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
    g.ipv4_addr = request.remote_addr
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
    g.ipv4_addr = request.remote_addr
    payload = request.get_json()

    if 'cur_password' not in keys:
        return Response(status=400)

    keys = payload.keys()
    update_info = {
        "uid":g.uid,
        "username":None,
        "cur_password":payload['cur_password'],
        "new_password":None,
        "is_manager":None
    }

    if 'username' in keys:
        update_info['username'] = payload['username']
    if 'new_password' in keys:
        update_info['new_password'] = payload['new_password']

    return services['User'].userinfo_update_service(**update_info)

# 회원 탈퇴
@login_required
@app.route("/withdraw", methods=["POST"])
def withdraw():
    g.ipv4_addr = request.remote_addr
    return services['User'].withdraw_service()

# 회원 리스트 조회
@login_required
@priv_required
@app.route("/get-users-metadata")
def get_users_metadata():
    g.ipv4_addr = request.remote_addr
    payload = request.get_json()
    keys = payload.keys()

    if 'only_manager' in keys:
        if keys['only_manager']:
            return services['User'].get_users_metadata_service_for_managing(only_manager=True)
        elif 'start' in keys and 'end' in keys:
            return services['User'].get_users_metadata_service_for_managing(start=payload['start'], end=payload['end'])
        else:
            return Response(status=400)
    else:
        return Response(status=400)

# 회원 권한 부여
@login_required
@priv_required
@app.route("/grant-privilege", methods=["POST"])
def grant_privilege():
    g.ipv4_addr = request.remote_addr
    payload = request.get_json()
    keys = payload.keys()

    if 'tgt_uid' not in keys:
        return Response(status=400)
    
    return services['User'].grant_priv_service(payload['tgt_uid'])

# 회원 권한 회수
@login_required
@priv_required
@app.route("/revoke-privilege", methods=["POST"])
def revoke_privilege():
    g.ipv4_addr = request.remote_addr
    payload = request.get_json()
    keys = payload.keys()

    if 'tgt_uid' not in keys:
        return Response(status=400)
    
    return services['User'].revoke_priv_service(payload['tgt_uid'])

# 회원 제재
@login_required
@priv_required
@app.route("/punish-user", methods=["POST"])
def punish_user():
    g.ipv4_addr = request.remote_addr
    payload = request.get_json()
    keys = payload.keys()

    if 'tgt_uid' not in keys:
        return Response(status=400)
    
    if 'block_until' in keys:
        return services['Punish'].punish_user_service(tgt_uid=payload['tgt_uid'], access_token=jwt_generator(
            g.uid,
            g.username,
            g.email,
            g.is_manager
        ))
    else:
        return services['Punish'].punish_user_service(tgt_uid=payload['tgt_uid'], block_until=payload['block_until'], access_token=jwt_generator(
            g.uid,
            g.username,
            g.email,
            g.is_manager
        ))
    
if __name__ == '__main__':
    init_database()
    app.run(host="127.0.0.1")