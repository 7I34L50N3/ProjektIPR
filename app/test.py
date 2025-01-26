from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import UserRepo, User
from group import GroupRepo, Group
import logging
import json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StudentApi:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StudentApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def student(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))
        return render_template('student.html')

    def register_routes(self, app):
        app.add_url_rule('/HomePage', 'student_dashboard', self.student_dashboard, methods=['GET'])
        app.add_url_rule('/marks', 'student_marks', self.marks, methods=['GET'])
        app.add_url_rule('/student', 'student', self.marks, methods=['GET'])

    def student_dashboard(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=session.get('user_id'))
        if user.get_role() != "student":
            flash("Nie masz uprawnień do tej strony", "error")
            return redirect(url_for('login'))

        user = user_repo.find_by_argument(username=session.get('user_id'))
        user_data = user.check_info()

        schedule = [
            {"time": day, "subject": group.check_info_group().get("language")}
            for group in user.groups
            for day in group.check_info_group().get("schedule")
        ]
        logger.info(schedule)

        student_data = {
            "user_id": user_data.get("id"),
            "schedule": schedule,
            "user_name": user_data.get("account")
        }

        return render_template('student_dashboard.html', **student_data)

    def marks(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=session.get('user_id'))
        if user.get_role() != "student":
            flash("Nie masz uprawnień do tej strony", "error")
            return redirect(url_for('login'))

        # Dane do wyświetlenia w szablonie

        groups = group.check_info_group().get('name')

        task_and_grades = {
            group.check_info_group().get("group_id"): [
                {"task": mark.description, "grade": mark.value}
                for mark in group.marks
                if mark.student_id == user.id  
            ]
            for group in user.groups
        }


        groups = ["Grupa 1", "Grupa 2", "Grupa 3"]
        tasks_and_grades = {
            "Grupa 1": [
                {"task": "Zadanie 1", "grade": "5"},
                {"task": "Zadanie 2", "grade": "4"},
            ],
            "Grupa 2": [
                {"task": "Zadanie 1", "grade": "3"},
                {"task": "Zadanie 2", "grade": "5"},
            ],
            "Grupa 3": [
                {"task": "Zadanie 1", "grade": "4"},
                {"task": "Zadanie 2", "grade": "4"},
            ],
        }

        # Domyślna grupa, np. Grupa 1
        selected_group = "Grupa 1"

        return render_template(
            'marks.html',
            groups=groups,
            tasks_and_grades=tasks_and_grades,
            selected_group=selected_group
        )