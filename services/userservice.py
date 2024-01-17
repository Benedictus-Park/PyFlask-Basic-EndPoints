import bcrypt
from flask import jsonify, Response

class UserService:
    def __init__(self, dao, token_generator):
        self.dao = dao
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
            rsp = Response(status=200)
            rsp.set_cookie(key='authorization', value=self.token_generator(
                u.uid,
                u.username,
                u.email,
                u.is_manager
            ))

            return rsp
        
    ##### 로그인 필요 #####
    def userinfo_update_service(self, uid:int, username:str=None, cur_password:str=None, new_password:str=None, is_manager:bool=None, force:bool=False, access_token:str=None) -> Response:    
        cur_userinfo = self.dao.get_user(uid=uid)

        if username != None:
            u = self.dao.get_user(username=username)
            if u != None:
                rsp = Response("중복 유저명 존재(Confilict)", status=409)
                rsp.set_cookie(key='authorization', value=self.token_generator(
                    u.uid,
                    u.username,
                    u.email,
                    u.is_manager
                ))
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
            rsp = Response(status=200)
            # 변경된 정보 반영하여 Token 재발급
            if access_token == None:
                rsp.set_cookie(key='authorization', value=self.token_generator(
                    u.uid,
                    u.username,
                    u.email,
                    u.is_manager
                ))
            else:
                rsp.set_cookie(key='authorization', value=access_token)

            return rsp
        
    def punish_user_service(self, tgt_uid:int, block_until:int=None, access_token:str=None) -> Response:
        if block_until == None:
            self.dao.update_uset(uid=tgt_uid, punished=True)
        else:
            self.dao.update_uset(uid=tgt_uid, punished=True, block_until=block_until)

        rsp = Response(status=200)
        rsp.set_cookie(key="authorization", value=access_token)

        return rsp