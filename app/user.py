import hashlib

from flask import Flask, render_template, request, redirect, url_for
class LoginApi:
    def __init__(self):
        self.app = Flask(__name__)
        self.add_routes()

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)

    def add_routes(self):
        self.app.add_url_rule('/', 'login', self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/success', 'success', self.success, methods=['GET'])
        self.app.add_url_rule('/failure', 'failure', self.failure, methods=['GET'])

    def login(self):
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            print(f'Username: {username} | Password: {password}')

            if username == "Admin" and password == "Admin":
                return redirect(url_for('success'))
            else:
                return redirect(url_for('failure'))

        return render_template("login.html")

    def success(self):
        # return render_template("vue_success.html")
        return render_template("success.html")

    def failure(self):
        return render_template("failure.html")


if __name__ == "__main__":
    app = LoginApi()
    app.run(debug=False, port=5000)