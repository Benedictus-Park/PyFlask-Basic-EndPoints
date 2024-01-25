import bcrypt
from ..app import jwt_generator
from ..daos import UserLogger
from flask import jsonify, Response

class UserService:
    def __init__(self, dao, userlogger:UserLogger, token_generator:jwt_generator):
        self.dao = dao
        self.logger = userlogger
        self.token_generator = token_generator

    def registration_service(self, username:str, email:str, password:str) -> Response:
        if self.dao.get_user(username=username) != None:
            return Response(response="이미 사용중인 사용자 이름입니다.(Confilict)", status=409)
        elif self.dao.get_user(email=email) != None:
            return Response(response="이미 사용중인 이메일입니다.(Confilict)", status=409)
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
            userinfo_dict = {
                'uid':int(u.uid),
                'username':str(u.username),
                'email':str(u.email),
                'is_manager':bool(u.is_manager),
            }

            rsp = jsonify(userinfo_dict)
            rsp.set_cookie(key='authorization', value=self.token_generator(u))

            return rsp
        
    def userinfo_update_service(self, uid:int, username:str=None, cur_password:str=None, new_password:str=None, is_manager:bool=None, force:bool=False) -> Response:    
        cur_userinfo = self.dao.get_user(uid=uid)

        if username != None:
            u = self.dao.get_user(username=username)
            if u != None:
                rsp = Response("중복 유저명 존재(Confilict)", status=409)
                rsp.set_cookie(key='authorization', value=self.token_generator(use_g=True))
                return rsp

        if cur_userinfo == None:
            return Response(status=400)
        elif not force and not bcrypt.checkpw(cur_password.encode('utf-8'), cur_userinfo.pwd.encode('utf-8')):
            return Response("패스워드 틀림.", status=401)
        
        if new_password != None:
            new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        u = self.dao.update_user(uid, username, new_password, is_manager)

        if u == None:
            return Response(status=400)
        else:
            userinfo_dict = {
                'uid':int(u.uid),
                'username':str(u.username),
                'email':str(u.email),
                'is_manager':bool(u.is_manager),
            }

            rsp = jsonify(userinfo_dict)
            rsp.set_cookie(key='authorization', value=self.token_generator(u))

            return rsp
    
    def get_users_metadata_service_for_managing(self, only_manager:bool=False, start:int=None, end:int=None) -> Response:
        count, users = self.dao.get_all_users_for_managing(only_manager)
        data = {
            "count":count,
            "only_manager":only_manager,
            "list":[]
        }

        if only_manager:
            for u in users:
                data['list'].append({
                    "uid":int(u.uid),
                    "username":str(u.username),
                    "email":str(u.email),
                    "created_at":str(u.created_at)
                })
        else:
            if start != None and end != None:
                users = users[start:end]

            for u in users:
                data['list'].append({
                    "uid":int(u.uid),
                    "username":str(u.username),
                    "email":str(u.email),
                    "is_manager":bool(u.is_manager),
                    "created_at":str(u.created_at),
                    "punished":bool(u.punished),
                    "blocked_until":str(u.blocked_until)
                })

        rsp = jsonify(data)
        rsp.set_cookie(key="authorization", vale=self.token_generator(use_g=True))

        return rsp
        