from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

app = Flask(__name__)



# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@127.0.0.1:3307/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicjalizacja SQLAlchemy
db = SQLAlchemy(app)

class User(db.model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def logout(self):
        # Implementacja mechanizmu wylogowania
        print(f"User {self.username} logged out.")

    def change_password(self, session, new_password):
        # Zmiana hasła użytkownika i zapis w bazie
        self.password = new_password
        session.commit()
        print(f"Password changed for user {self.username}.")

    def check_info(self):
        # Zwracanie informacji o użytkowniku
        return {
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "surname": self.surname
        }

class UserRepo:
    def __init__(self, session):
        self.session = session

    def find(self):
        # Pobiera wszystkich użytkowników
        return self.session.query(User).all()

    def create(self, username, password, email, name, surname):
        # Tworzy nowego użytkownika
        user = User(username=username, password=password, email=email, name=name, surname=surname)
        self.session.add(user)
        self.session.commit()
        return user

    def find_by_argument(self, **kwargs):
        # Wyszukuje użytkownika na podstawie argumentów (np. username, email)
        try:
            return self.session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            return None

    def update(self, user_id, **kwargs):
        # Aktualizuje dane użytkownika
        user = self.session.query(User).get(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()
        return user

    def delete(self, user_id):
        # Usuwa użytkownika
        user = self.session.query(User).get(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()

    def login(self, username, password):
        # Logowanie użytkownika
        user = self.session.query(User).filter_by(username=username, password=password).first()
        if user:
            return user
        else:
            return None




