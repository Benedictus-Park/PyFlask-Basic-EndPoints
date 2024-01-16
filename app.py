from flask_cors import CORS
from flask import Flask, request, g

# 사용자 정의 모듈/패키지
from daos import *
from services import *
from decorators import *
from database import db_session
from config import JWT_SECRET_KEY

app = Flask(__name__)
CORS(app)

services = dict()
services['User'] = UserService(UserDao(db_session), JWT_SECRET_KEY)

# 회원가입 처리 Endpoint
@app.route("/registration", methods=["POST"])
def registration():
    payload = request.get_json()
    
    username = payload['username']
    email = payload['email']
    password = payload['password']

    pass

# 로그인 처리 Endpoint
@app.route("/authenticate", methods=["POST"])
def authenticate():
    payload = request.get_json()

    email = payload['email']
    password = payload['password']

    pass
