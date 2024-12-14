import hashlib
class User:
    def __init__(self, username: str, password: str):
        self.__username = None
        self.__hashed_password = None

        if username:
            self.__username = username

        if password:
            self.__hashed_password = hashlib.sha512(password.encode()).hexdigest()

    def login(self, login: str, password: str):
        hash = hashlib.sha512(password.encode())

        if self.__username == login and self.__hashed_password == hash.hexdigest():
            return True
        else:
            return False