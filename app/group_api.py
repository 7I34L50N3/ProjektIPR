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

        user_repo = UserRepo()
        user = user_repo.find_by_argument(username=session.get('user_id'))
        if user.get_role() != "admin":
            flash("Nie masz uprawnień do tej strony", "error")
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
                "Sr. 8:00", "Sr. 10:00", "Sr. 12:00", "Sr. 14:00", "Sr. 16:00",
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
        return render_template("groups.html", **groups_data)

    def edit(self):
        data = request.json
        id = data.get('id')
        name = data.get('group_id')
        language = data.get('language')
        schedule = json.dumps(data.get('schedule', []))
        students_ids = data.get('students', [])

        group_repo = GroupRepo()
        user_repo = UserRepo()

        group = group_repo.find_by_argument(id=id)
        if not group:
            return jsonify({"message": "Grupa nie istnieje!"}), 400


        group_repo.update(id,name=name,language=language, schedule=schedule)

        group.clear_users()

        for student_id in students_ids:
            student = user_repo.find_by_argument(id=student_id)
            if student:
                student.add_group(group)
            else:
                logger.warning(f"Student ID {student_id} not found.")

        db.session.commit()

        return jsonify({"message": "Grupa została zmodyfikowana!"}), 200

    def add(self):
        data = request.json
        #
        name = data.get('group_id')
        language = data.get ('language')
        schedule = json.dumps(data.get('schedule', []))
        students_ids = data.get('students',[])

        group_repo = GroupRepo()
        user_repo = UserRepo()
        existing_group=group_repo.find_by_argument(name=name)
        if existing_group:
            return jsonify({"message": "Taka grupa już istnieje"}), 400

        new_group = group_repo.create(name, language, schedule)

        db.session.add(new_group)
        db.session.commit()
        #db.session
        for student_id in students_ids:
            logger.info(f"Processing student ID: {student_id}")
            student = user_repo.find_by_argument(id=student_id)
            if student:
                student.add_group(new_group)

        db.session.commit()

        logger.info(data)
        return jsonify({"message": "Grupa została dodana!"}), 200