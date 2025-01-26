from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import UserRepo, user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StudentApi:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StudentApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/HomePage', 'student_dashboard', self.student_dashboard, methods=['GET'])
        app.add_url_rule('/marks', 'student_marks', self.marks, methods=['GET'])

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

        schedule = [
            {"time": "8:00 - 9:00", "subject": "Matematyka"},
            {"time": "9:00 - 10:00", "subject": "Angielski"},
            {"time": "10:15 - 11:15", "subject": "Biologia"},
            {"time": "11:30 - 12:30", "subject": "Historia"},
        ]

        student_data = {
            "user_id": user_id,
            "schedule": schedule,
            "user_name": "Dawid Jasper Wójcik",
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