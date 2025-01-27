import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import UserRepo, User
from student import Student
from group import Group,GroupRepo
from admin import Admin
from globals import app, db
from hashlib import sha256
import json

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
        app.add_url_rule('/student', 'student', self.student, methods=['GET'])

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

        groups = user.get_groups()
        groups_text = [group.check_info_group().get("group_id") for group in groups]

        tasks_and_grades = {
            group.check_info_group().get("group_id"): [
                {"task": mark.check_info_mark().get("description"), "grade": mark.check_info_mark().get("value")}
                for mark in group.get_marks()
                if mark.check_info_mark().get("student_id") == user.check_info().get("id")
            ]
            for group in groups
        }

        if groups.count() > 0:
            selected_group = groups[0].check_info_group().get("group_id")
        else:
            selected_group = None

        return render_template(
            'marks.html',
            groups=groups_text,
            tasks_and_grades=tasks_and_grades,
            selected_group=selected_group
        )

    def student(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))
        return render_template('student.html')