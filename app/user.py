from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.exc import OperationalError, NoResultFound
from sqlalchemy.orm import relationship
from group import Group, GroupRepo
from globals import app, db, user_group_association
from hashlib import sha256
from datetime import datetime

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)  # Dodano długość VARCHAR
    password = Column(String(100), nullable=False)  # Dodano długość VARCHAR
    email = Column(String(100), nullable=False, unique=True)  # Dodano długość VARCHAR
    name = Column(String(50), nullable=False)  # Dodano długość VARCHAR
    surname = Column(String(50), nullable=False)  # Dodano długość VARCHAR
    role = Column(String(50), nullable=False)  # Dodano długość VARCHAR
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    groups = relationship('Group', secondary=user_group_association, back_populates='users', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role,
        'with_polymorphic': '*'
    }

    def change_password(self, new_password):
        new_password = sha256(new_password.encode()).hexdigest()
        self.password = new_password
        db.session.commit()
        print(f"Password changed for user {self.username}.")

    def check_info(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.name,
            "last_name": self.surname,
            "role": self.role,
            "account": self.username,
            "password": "*****",
            "added_date": str(self.created_at)
        }
    def get_role(self):
        return self.role

    def add_group(self, group):
        self.groups.append(group)
        db.session.commit()

    def get_groups(self):
        return self.groups

class UserRepo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRepo, cls).__new__(cls)
        return cls._instance

    def find(self):
        return db.session.query(User).all()

    def create(self, username, password, email, name, surname, role):
        password = sha256(password.encode()).hexdigest()
        user = User(username=username, password=password, email=email, name=name, surname=surname, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    def find_by_argument(self, **kwargs):
        try:
            return db.session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            return None

    def update(self, user_id, **kwargs):
        user = db.session.query(User).get(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if key == 'password':
                logger.info(f"Password changed for user {user.username}., {value}")
                value = sha256(value.encode()).hexdigest()
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    def login(self, username, password):
        user = db.session.query(User).filter_by(username=username).first()

        password = sha256(password.encode()).hexdigest()
        if user and user.password == password:
            return user
        else:
            return None