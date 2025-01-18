import hashlib
class UserRepo:
    def __init__(self, username: str, password: str):
        self._username = None
        self._hashed_password = None

        if username:
            self._username = username

        if password:
            self._hashed_password = hashlib.sha512(password.encode()).hexdigest()

    def login(self, login: str, password: str):
        hash = hashlib.sha512(password.encode())

        if self._username == login and self._hashed_password == hash.hexdigest():
            return True
        else:
            return False