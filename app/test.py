from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

class GroupApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GroupApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register_routes(self, app):
        app.add_url_rule('/groups', 'groups', self.groups, methods=['GET'])

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
                    "schedule": "Śr. 15:40",
                    "student_ids": [1],
                    "students": ["Wanda"]
                }
            ],
            "all_students": [
                {"id": 1, "first_name": "Wanda", "last_name": "Narkiewicz"},
                {"id": 2, "first_name": "Karolina", "last_name": "Nowak"},
                {"id": 3, "first_name": "Waldek", "last_name": "Kowalski"},
                {"id": 4, "first_name": "Jędrzej", "last_name": "Bąk"}
            ]
        }
        return render_template("groups.html", **groups_data)