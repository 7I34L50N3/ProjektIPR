import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import UserRepo, User
from student import Student
from admin import Admin
from globals import app
from hashlib import sha256

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppControler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppControler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.app = app
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)
        module.register_routes(self.app)

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)


class LoginApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoginApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.secret_key = os.urandom(24)
        app.add_url_rule('/', 'login', self.login, methods=['GET', 'POST'])

    def login(self):
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user_repo = UserRepo()
            user = user_repo.login(username, password)

            if user is None:
                flash("Nieprawidłowy login lub hasło", "error")
                return render_template("login.html")
            if(user.get_role() == "student"):
                session['user_id'] = username
                pass
            elif(user.get_role() == "admin"):
                session['user_id'] = username
                return redirect(url_for('admin_dashboard'))
            else:
                flash("Nieprawidłowy login lub hasło", "error")

        return render_template("login.html")


class LogoutApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LogoutApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])

    def logout(self):
        session.pop('user_id', None)  # Usuń użytkownika z sesji
        flash("Zostałeś wylogowany.", "info")
        return redirect(url_for('login'))


class ChangePasswordApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChangePasswordApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/change_password', 'change_password', self.change_password, methods=['POST', 'GET'])

    def change_password(self):
        if request.method == 'POST':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if new_password != confirm_password:
                flash("Nowe hasła nie są takie same", "error")
                return redirect(url_for('change_password'))

            user_repo = UserRepo()
            user = user_repo.find_by_argument(username=session.get('user_id'))
            if user is None:
                flash("Użytkownik nie istnieje", "error")
                return redirect(url_for('change_password'))

            hashed_password = sha256(current_password.encode()).hexdigest()
            if user.password != hashed_password:
                flash("Nieprawidłowe obecne hasło", "error")
                return redirect(url_for('change_password'))

            user.change_password(new_password)
            flash("Hasło zostało zmienione", "info")
            print(f'{current_password} | {new_password} | {confirm_password}')

        return redirect(url_for('account_info'))


class AdminApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AdminApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/dashboard', 'admin_dashboard', self.admin_dashboard, methods=['GET'])
        app.add_url_rule('/account', 'account_info', self.account_info, methods=['GET'])

    def admin_dashboard(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=session.get('user_id'))
        if user.get_role() != "admin":
            flash("Nie masz uprawnień do tej strony", "error")
            return redirect(url_for('login'))

        dashboard_data = {
            'username': user_id,
            'students': 50,
            'teachers': 4,
            'groups': 5
        }
        return render_template("admin_dashboard.html", **dashboard_data)

    def account_info(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=session.get('user_id'))
        user_data = {
            'role': 'Administrator',
            'first_name': 'Ryszard',
            'last_name': 'Wójcik',
            'email': f'ryszard.wojcik@lingduo.edu.pl',
            'added_date': '16.12.2024',
        }
        return render_template("account_info.html", **user_data)


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