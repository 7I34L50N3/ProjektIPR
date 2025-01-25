from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

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
        app.add_url_rule('/home', 'student_dashboard', self.student_dashboard, methods=['GET'])

    def student_dashboard(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        return render_template('student_dashboard.html')