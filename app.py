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
        access_token = request.cookies.get("authorization")

        if access_token is None:
            return Response(status=400)
        else:
            try:
                payload = jwt.decode(access_token, JWT_SECRET_KEY, 'HS256')
            except Exception:
                return Response(response="유효하지 않은 토큰", status=401)
            
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
            return Response(response="권한 없음.", status=401)
        return f(*args, **kwargs)
    return wrapper

sys.path.insert(1, os.path.abspath('.'))

app = Flask(__name__)
CORS(app)

logger = Logger(db_session)

services = dict()
services['User'] = UserService(UserDao(db_session), logger, jwt_generator)
services['Punish'] = PunishService(UserDao(db_session), logger, jwt_generator)

# db_robot = Robot(logger, db_session)
# db_robot.start()

# 회원가입 처리 Endpoint
@app.route("/registration", methods=["POST"])
def registration():
    g.ipv4_addr = request.remote_addr
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
    email = request.authorization.get("username")
    password = request.authorization.get("password")

    return services['User'].authentication_service(email, password)

# 회원정보(유저명, 패스워드) 업데이트, 권한 업데이트는 지원하지 않음.
@app.route("/update-userinfo", methods=["PATCH"])
@login_required
def update_userinfo():
    g.ipv4_addr = request.remote_addr
    payload = request.get_json()
    keys = payload.keys()

    if 'cur_password' not in keys:
        return Response(status=400)

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
@app.route("/withdraw", methods=["PATCH"])
@login_required
def withdraw():
    g.ipv4_addr = request.remote_addr
    return services['User'].withdraw_service(g.uid)

# 회원 리스트 조회
@app.route("/get-users-metadata", methods=["GET"])
@login_required
@priv_required
def get_users_metadata():
    g.ipv4_addr = request.remote_addr
    only_manager = request.args.get("only_manager", type=int)

    return services['User'].get_users_metadata_service_for_managing(only_manager=bool(only_manager))

# 회원 권한 부여
@app.route("/grant-privilege", methods=["PATCH"])
@login_required
@priv_required
def grant_privilege():
    g.ipv4_addr = request.remote_addr
    tgt_uid = request.args.get("tgt_uid", type=int)
    
    return services['User'].grant_priv_service(tgt_uid)

# 회원 권한 회수
@app.route("/revoke-privilege", methods=["PATCH"])
@login_required
@priv_required
def revoke_privilege():
    g.ipv4_addr = request.remote_addr
    tgt_uid = request.args.get("tgt_uid", type=int)
    
    return services['User'].revoke_priv_service(tgt_uid)

# 회원 제재
@app.route("/punish-user", methods=["POST"])
@login_required
@priv_required
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
    app.run(host="127.0.0.1", debug=True)