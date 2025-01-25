import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import UserRepo, User
from student import Student
from group import Group
from admin import Admin
from globals import app, db
from hashlib import sha256

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class UserApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/users', 'users', self.users, methods=['GET'])
        app.add_url_rule('/add_user', 'add_user', self.add_user, methods=['POST'])
        app.add_url_rule('/edit_user', 'edit_user', self.edit_user, methods=['POST'])

    def users(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        users_data = {
            "users": [
                {"id": 1, "first_name": "Wanda", "last_name": "Narkiewicz", "role": "Student", "account": "wannar01", "password": "*****"},
                {"id": 2, "first_name": "Adam", "last_name": "Kowalski", "role": "Teacher", "account": "adamkow", "password": "*****"}
            ]
        }
        return render_template("users.html", **users_data)

    def add_user(self):
        user_data = request.get_json()
        logger.info(user_data)
        return jsonify({"message": "Użytkownik został dodany pomyślnie!"}), 200

    def edit_user(self):
        user_data = request.get_json()
        logger.info(user_data)
        return jsonify({"message": "Zmiany zapisane pomyślnie!"}), 200