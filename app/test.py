from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

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

    def groups(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        groups_data = {
            "groups": [
                {
                    "id": 1,
                    "group_id": "021_WT",
                    "language": "Niemiecki",
                    "teacher": "Adolf H.",
                    "teacher_id": 1,  # ID nauczyciela
                    "schedule": "Śr. 15:40",
                    "student_ids": [1, 2],
                    "students": ["Wanda", "Karolina"]
                }
            ],
            "all_students": [
                {"id": 1, "first_name": "Wanda", "last_name": "Narkiewicz"},
                {"id": 2, "first_name": "Karolina", "last_name": "Nowak"},
                {"id": 3, "first_name": "Waldek", "last_name": "Kowalski"},
                {"id": 4, "first_name": "Jędrzej", "last_name": "Bąk"}
            ],
            "all_teachers": [
                {"id": 1, "first_name": "Adolf", "last_name": "H."},
                {"id": 2, "first_name": "Anna", "last_name": "Kowalska"},
                {"id": 3, "first_name": "Jan", "last_name": "Nowak"}
            ],
            "all_schedules": ["Pn. 9:00", "Śr. 15:40", "Pt. 18:00"],
            "all_languages": ["Niemiecki", "Angielski", "Francuski", "Hiszpański"]
        }
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
