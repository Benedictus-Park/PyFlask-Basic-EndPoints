from sqlalchemy.sql import text
from sqlalchemy.engine import Engine

class UserDao:
    def __init__(self, engine:Engine):
        self.engine = engine

    # Hashed Password가 Parameter로 주어져야 함에 유의.
    def insert_user(self, username:str, email:str, password:str) -> int:
        param = {
            "username":username,
            "email":email,
            "password":password
        }

        