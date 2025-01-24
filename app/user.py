from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.exc import OperationalError, NoResultFound

app = Flask(__name__)

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@127.0.0.1:3307/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)  # Dodano długość VARCHAR
    password = Column(String(100), nullable=False)  # Dodano długość VARCHAR
    email = Column(String(100), nullable=False, unique=True)  # Dodano długość VARCHAR
    name = Column(String(50), nullable=False)  # Dodano długość VARCHAR
    surname = Column(String(50), nullable=False)  # Dodano długość VARCHAR

    def logout(self):
        print(f"User {self.username} logged out.")

    def change_password(self, session, new_password):
        self.password = new_password
        session.commit()
        print(f"Password changed for user {self.username}.")

    def check_info(self):
        return {
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "surname": self.surname
        }

class UserRepo:
    _instance = None

    def __new__(cls, session):
        if cls._instance is None:
            cls._instance = super(UserRepo, cls).__new__(cls)
            cls._instance.session = session
        return cls._instance

    def find(self):
        return self.session.query(User).all()

    def create(self, username, password, email, name, surname):
        user = User(username=username, password=password, email=email, name=name, surname=surname)
        self.session.add(user)
        self.session.commit()
        return user

    def find_by_argument(self, **kwargs):
        try:
            return self.session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            return None

    def update(self, user_id, **kwargs):
        user = self.session.query(User).get(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()
        return user

    def delete(self, user_id):
        user = self.session.query(User).get(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()

    def login(self, username, password):
        user = self.session.query(User).filter_by(username=username, password=password).first()
        if user:
            return user
        else:
            return None

    @staticmethod
    def create_tables():
        db.create_all()
        print("Tables created successfully.")

if __name__ == "__main__":


        # Wyświetlenie wszystkich użytkowników
        users = user_repo.find()
        for user in users:
            print(user.check_info())
