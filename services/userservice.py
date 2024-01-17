import jwt
import bcrypt
from flask import jsonify, Response
from datetime import datetime, timedelta

# for Developement
from ..daos.userdao import UserDao

class UserService:
    def __init__(self, dao:UserDao, JWT_KEY:str):
        self.dao = dao
        self.JWT_KEY = JWT_KEY

    def registration_service(self, username:str, email:str, password:str) -> Response:
        if self.dao.get_user(username=username) != None:
            return Response(response="이미 사용중인 사용자 이름입니다.", status=400)
        elif self.dao.get_user(email=email) != None:
            return Response(response="이미 사용중인 이메일입니다.", status=400)
        else:
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            self.dao.insert_user(username, email, password)
            return Response(status=200)
        
    def authentication_service(self, email:str, password:str) -> Response:
        u = self.dao.get_user(email=email)

        if u == None:
            return Response(status=401)
        elif bcrypt.checkpw(password.encode('utf-8'), u.pwd.encode('utf-8')) == False:
            return Response(status=401)
        else:
            # Token 유효 시간 : 1시간
            exp = datetime.utcnow() + timedelta(hours=1)

            access_token = jwt.encode({
                'uid':u.uid,
                'username':u.username,
                'email':u.email,
                'is_manager':u.is_manager,
                'exp':exp
            }, self.JWT_KEY, algorithm='HS256')

            rsp = Response(status=200)
            rsp.set_cookie(key='authorization', value=access_token)

            return rsp
        
    def userinfo_update_service(self, uid:int, username:str=None, cur_password:str=None, new_password:str=None, is_manager:bool=None) -> Response:    
        cur_userinfo = self.dao.get_user(uid=uid)

        if cur_userinfo == None:
            return Response(status=400)
        elif not bcrypt.checkpw(cur_password.encode('utf-8'), cur_userinfo.pwd.encode('utf-8')):
            return Response("패스워드 틀림.", status=401)
        
        if new_password != None:
            new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        u = self.dao.update_user(uid, username, new_password, is_manager)

        if u == None:
            return Response(status=400)
        else:
            # Token 유효 시간 : 1시간
            # 변경된 정보 반영하여 Token 재발급
            exp = datetime.utcnow() + timedelta(hours=1)

            access_token = jwt.encode({
                'uid':uid,
                'username':u.username,
                'email':u.email,
                'is_manager':u.is_manager,
                'exp':exp
            }, self.JWT_KEY, algorithm='HS256')

            rsp = Response(status=200)
            rsp.set_cookie(key='authorization', value=access_token)

            return rsp
        
    def user_remove_service(self, uid:int) -> Response:
        self.dao.delete_user(uid=uid)
        return Response(status=200)