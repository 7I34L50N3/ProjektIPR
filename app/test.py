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
        app.add_url_rule('/test', 'test', self.logout, methods=['GET'])

    def logout(self):
        session.pop('user_id', None)  # Usuń użytkownika z sesji
        flash("Zostałeś wylogowany.", "info")
        return redirect(url_for('login'))