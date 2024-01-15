import jwt
import bcrypt
import datetime
from flask import jsonify, Response

class UserService:
    def __init__(self, dao, JWT_KEY:str):
        self.dao = dao
        self.JWT_KEY = JWT_KEY
