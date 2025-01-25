import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import UserRepo, User
from student import Student
from group import Group,GroupRepo
from admin import Admin
from globals import app, db
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
                return redirect(url_for('student_dashboard'))
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

class AccountInfoApi:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AccountInfoApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/account', 'account_info', self.account_info, methods=['GET'])
        app.add_url_rule('/home', 'home', self.home, methods=['GET'])

    def home(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=user_id)
        role = user.get_role()

        if not user:
            flash("Nie znaleziono użytkownika", "error")
            return redirect(url_for('login'))

        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'student':
            return redirect(url_for('student_dashboard'))
        else:
            return redirect(url_for('login'))

    def account_info(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=session.get('user_id'))
        user_data = user.check_info()

        return render_template("account_info.html", **user_data)


class AdminApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AdminApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/AdminDashboard', 'admin_dashboard', self.admin_dashboard, methods=['GET'])

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

        students_count = db.session.query(Student).count()
        groups_count = db.session.query(Group).count()

        dashboard_data = {
            'username': user_id,
            'students': students_count,
            'teachers': 4,
            'groups': groups_count
        }
        return render_template("admin_dashboard.html", **dashboard_data)




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
        all_user = user_repo.find()
        users_data = {
            "users": [user.check_info() for user in all_user]}
        return render_template("users.html", **users_data)

    def add_user(self):
        user_data = request.get_json()
        username = user_data.get('account')
        password = user_data.get('password')
        password = sha256(password.encode()).hexdigest()
        name = user_data.get('first_name')
        surname = user_data.get('last_name')
        role = user_data.get('role')
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
        username = user_data.get('account')
        password = user_data.get('password')
        password = sha256(password.encode()).hexdigest()
        name = user_data.get('first_name')
        surname = user_data.get('last_name')
        role = user_data.get('role')

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=username)
        user_id = user.check_info().get('id')

        update_data={"username":username, "passowrd": password, "name":name, "surname":surname, "role":role}
        user_repo.update( user_id,**update_data)


        return jsonify({"message": "Zmiany zapisane pomyślnie!"}), 200


class GroupApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GroupApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/groups', 'groups', self.groups, methods=['GET'])
        app.add_url_rule('/edit_group', 'edit_group', self.edit, methods=['POST'])
        app.add_url_rule('/add_group', 'add_group', self.add, methods=['POST'])

    def groups(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        group_repo = GroupRepo()
        all_groups = group_repo.find()
        user_repo = UserRepo()
        all_users = user_repo.find()
        all_students = [user.check_info() for user in all_users if user.get_role() == "student"]

        groups_data = {
            "groups": [
                {
                    **group.check_info_group(),
                    "students_ids": [user.check_info().get("id") for user in group.users],
                    "students": [f"{user.check_info().get('first_name')} {user.check_info().get('last_name')}" for user in group.users],
                    "teacher": "Aneta Glapinska"
                }
                for group in all_groups
            ],
            "all_schedules": [
                "Pn. 8:00", "Pn. 10:00", "Pn. 12:00", "Pn. 14:00", "Pn. 16:00",
                "Wt. 8:00", "Wt. 10:00", "Wt. 12:00", "Wt. 14:00", "Wt. 16:00",
                "Śr. 8:00", "Śr. 10:00", "Śr. 12:00", "Śr. 14:00", "Śr. 16:00",
                "Czw. 8:00", "Czw. 10:00", "Czw. 12:00", "Czw. 14:00", "Czw. 16:00",
                "Pt. 8:00", "Pt. 10:00", "Pt. 12:00", "Pt. 14:00", "Pt. 16:00"
            ],
            "all_students": [
                {
                    "id": student.get("id"),
                    "first_name": student.get("first_name"),
                    "last_name": student.get("last_name")
                }
                for student in all_students
            ],
            "all_teachers": [
                {"id": 1, "first_name": "Aneta", "last_name": "Glapinska"},
                {"id": 2, "first_name": "Ryszard", "last_name": "Małejaja"},
                {"id": 3, "first_name": "Bartosz", "last_name": "Władziński"}
            ],
            "all_languages": ["Niemiecki", "Angielski", "Francuski", "Hiszpański"]


        }

            #"groups": [Group.check_info_group() for Group in all_groups]}

        #     "groups": [
        #         {
        #             #group.check_info_group() for group in all_groups
        #             # "id": 1,
        #             # "group_id": "021_WT",
        #             # "language": "Niemiecki",
        #             # "teacher": "Adolf H.",
        #             # "teacher_id": 1,  # ID nauczyciela
        #             # "schedule": "Śr. 15:40",
        #             # "student_ids": [1, 2],
        #             # "students": ["Wanda", "Karolina"]
        #         }
        #     ],
        #     "all_students": [
        #
        #         # {"id": 1, "first_name": "Wanda", "last_name": "Narkiewicz"},
        #         # {"id": 2, "first_name": "Karolina", "last_name": "Nowak"},
        #         # {"id": 3, "first_name": "Waldek", "last_name": "Kowalski"},
        #         # {"id": 4, "first_name": "Jędrzej", "last_name": "Bąk"}
        #     ],
        #     "all_teachers": [
        #         {"id": 1, "first_name": "Adolf", "last_name": "H."},
        #         {"id": 2, "first_name": "Anna", "last_name": "Kowalska"},
        #         {"id": 3, "first_name": "Jan", "last_name": "Nowak"}
        #     ],
        #     "all_schedules": ["Pn. 9:00", "Śr. 15:40", "Pt. 18:00"],
        #     "all_languages": ["Niemiecki", "Angielski", "Francuski", "Hiszpański"]
        # }
        return render_template("groups.html", **groups_data)

    def edit(self):
        data = request.json

        group_data = {
            "group_id": data.get('group_id'),
            "language": data.get('language'),
            "teacher": data.get('teacher'),
            "schedule": data.get('schedule'),
            "student_ids": data.get('students')
        }
        logger.info(group_data)
        return jsonify({"message": "Grupa została zmodyfikowana!"}), 200

    def add(self):
        data = request.json
        #
        name = data.get('group_id')
        language = data.get ('language')
        schedule = data.get('schedule')
        students_ids = data.get('students_ids',[])

        group_repo = GroupRepo()
        user_repo = UserRepo()
        existing_group=group_repo.find_by_argument(name=name)
        if existing_group:
            return jsonify({"message": "Taka grupa już istnieje"})

        new_group = group_repo.create(name, language, schedule)


        for student_id in students_ids:
            student = user_repo.find_by_argument(id=student_id)
            if student:
                student.add_group(new_group)


        db.session.add(new_group)
        db.session
        logger.info(data)
        return jsonify({"message": "Grupa została dodana!"}), 200