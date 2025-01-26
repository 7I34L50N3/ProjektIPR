import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import UserRepo, User
from student import Student
from group import Group,GroupRepo
from admin import Admin
from globals import app, db
from hashlib import sha256
import json



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
