from typing import Dict
from bcrypt import gensalt, hashpw, checkpw

UserType=Dict[str, str]

class Error(Exception):
    """Base class for other exceptions"""
    pass

class UserNotFoundException(Error):
    """Raised when no user with provided details are found (i.e., no user for username)"""
    pass

class Auth:
    def __init__(self, conn):
        self.conn=conn
    def register(self, user: UserType):
        salt=gensalt()
        user.password=hashpw(user.password.encode("utf-8"), salt)
        params={"username": user.username, "password": user.password}
        c=self.conn.cursor()
        c.execute("INSERT INTO users VALUES(:username, :password)", params)
        self.conn.commit()
        return True
    def login(self, user: UserType):
        result=self.conn.execute("SELECT FROM users WHERE(username=:username)", {"username": user.username})
        c=self.conn.cursor()
        result=c.fetchone()
        if result==None:
            raise UserNotFoundException
        if checkpw(user.password.encode("utf-8"), result['password']):
            return True
        else:
            return False

