from sqlalchemy.orm import scoped_session

class Robot:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def start(self):
        pass