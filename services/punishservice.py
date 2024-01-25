from ..app import jwt_generator
from ..daos import Logger
from flask import jsonify, Response, g

class PunishService:
    def __init__(self, userdao, logger:Logger, token_generator:jwt_generator):
        self.userdao = userdao
        self.logger = logger
        self.token_generator = token_generator

    def punish_user_service(self, tgt_uid:int, block_until:int=None) -> Response:
        if block_until == None:
            self.userdao.update_user(uid=tgt_uid, punished=True)
        else:
            self.userdao.update_user(uid=tgt_uid, punished=True, block_until=block_until)

        rsp = Response(status=200)
        rsp.set_cookie(key="authorization", value=self.token_generator(use_g=True))

        self.logger.punish_user(g.uid, tgt_uid)

        return rsp