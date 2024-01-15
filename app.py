from flask_cors import CORS
from flask import Flask, request, g

# 사용자 정의 모듈/패키지
from database.database import *
from decorators import *

# Service, Data Access Object 통합 관리용 더미 클래스
class Flask_App:
    def __init__(self):
        self.services = dict()
        self.daos = dict()

app = Flask(__name__)
CORS(app)

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
