import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import UserRepo, User
from student import Student
from group import Group,GroupRepo
from admin import Admin
from globals import app, db
from hashlib import sha256
import json

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

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=session.get('user_id'))
        if user.get_role() != "admin":
            flash("Nie masz uprawnień do tej strony", "error")
            return redirect(url_for('login'))

        user_repo = UserRepo()
        all_user = user_repo.find()
        users_data = {
            "users": [user.check_info() for user in all_user]}
        return render_template("users.html", **users_data)

    def add_user(self):
        user_data = request.get_json()
        username = user_data.get('account')
        password = user_data.get('password')
        name = user_data.get('first_name')
        surname = user_data.get('last_name')
        role = user_data.get('role')
        if role != "admin" and role != "student":
            return jsonify({"message": "Użytkownik o nieobsługiwanej roli"}), 400
        email = f"{username.lower()}@lingduo.com"

        user_repo = UserRepo()
        existing_user = user_repo.find_by_argument(username=username)
        if existing_user:
            return jsonify({"message": "Użytkownik o takim username już istnieje!"}), 400

        user = user_repo.create(username, password, email, name, surname, role)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Użytkownik został dodany pomyślnie!"}), 200

    def edit_user(self):
        user_data = request.get_json()
        user_id = user_data.get('id')
        username = user_data.get('account')
        password = user_data.get('password')
        name = user_data.get('first_name')
        surname = user_data.get('last_name')
        role = user_data.get('role')
        if role != "admin" and role != "student":
            return jsonify({"message": "Użytkownik o nieobsługiwanej roli"}), 400
        user_repo = UserRepo()

        update_data={"username":username, "password": password, "name":name, "surname":surname, "role":role}
        user_repo.update(user_id,**update_data)


        return jsonify({"message": "Zmiany zapisane pomyślnie!"}), 200