from typing import TypedDict
from bcrypt import gensalt, hashpw, checkpw

class UserType(TypedDict):
    username: str
    password: str

class Error(Exception):
    """Base class for other exceptions"""
    pass

class UserAlreadyExistsException(Error):
    """Raised when a user already exists with the provided credentials (i.e., user with username already exists)"""

class UserNotFoundException(Error):
    """Raised when no user with provided details are found (i.e., no user for username)"""
    pass

class Auth:
    def __init__(self, conn):
        self.conn=conn
    
    def check_if_user_exists(self, username: str):
        c=self.conn.cursor()
        c.execute("SELECT * FROM users WHERE username=:username", {'username':username})
        result=c.fetchone()
        if not result==None:
            return True
        else:
            return False

    def register(self, user: UserType):
        if self.check_if_user_exists(user['username']):
            raise UserAlreadyExistsException

        salt=gensalt()
        user['password']=hashpw(user['password'].encode("utf-8"), salt)
        params={"username": user['username'], "password": user['password']}
        c=self.conn.cursor()
        c.execute("INSERT INTO users(username, password) VALUES(:username, :password)", params)
        self.conn.commit()
        return True

    def login(self, user: UserType):
        result=self.conn.execute("SELECT FROM users WHERE(username=:username)", {"username": user['username']})
        c=self.conn.cursor()
        result=c.fetchone()
        if result==None:
            raise UserNotFoundException
        if checkpw(user.password.encode("utf-8"), result['password']):
            return True
        else:
            return False

