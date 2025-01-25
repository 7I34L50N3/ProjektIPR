import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from globals import app, db, user_group_association
import json


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    language = db.Column(db.String(255), nullable=True)
    users = relationship('User', secondary=user_group_association, back_populates='groups', lazy='dynamic')
    schedule = db.Column(db.Text, nullable=True)
    marks = relationship('Mark', back_populates='group', lazy='dynamic')
    def check_info_group(self):
        return {
            "id": self.id,
            "group_id": self.name,
            "language": self.language,
            "schedule": json.loads(self.schedule)
        }
    def __repr__(self):
        return f"<Group {self.name}>"


# Repozytorium grup
class GroupRepo:
    _instance = None  # Atrybut klasy przechowujący jedyną instancję

    def __new__(cls, *args, **kwargs):
        if not cls._instance:  # Jeśli instancja jeszcze nie istnieje, twórz ją
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def create(self, name, language=None,schedule=None):
        new_group = Group(name=name,  language=language ,schedule=schedule)
        db.session.add(new_group)
        db.session.commit()
        return new_group

    def update(self, group_id, name=None, language=None, schedule=None):
        group = Group.query.get(group_id)
        if group:
            if name:
                group.name = name
            if language:
                group.language = language
            if schedule:
                group.schedule = schedule
            db.session.commit()
        return group

    def find_by_argument(self, **kwargs):
        return Group.query.filter_by(**kwargs).one()


    def delete(self, group_id):
        group = Group.query.get(group_id)
        if group:
            db.session.delete(group)
            db.session.commit()
        return group

    def find(self):
        #zwraca wszystkie grupy
        return Group.query.all()


if __name__ == '__main__':
    with app.app_context():


        app.run(debug=True)

















