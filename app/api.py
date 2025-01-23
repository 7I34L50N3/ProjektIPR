from flask import Flask, render_template, request, redirect, url_for, flash

class AppControler:
    def __init__(self):
        self.app = Flask(__name__)
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)
        module.register_routes(self.app)

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)


class LoginApi:
    def __init__(self):
        self.name = "LoginApi"

    def register_routes(self, app):
        app.secret_key = "secret_key"
        app.add_url_rule('/', 'login', self.login, methods=['GET', 'POST'])
        app.add_url_rule('/success', 'success', self.success, methods=['GET'])

    def login(self):
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            print(f'Username: {username} | Password: {password}')

            if username == "Admin" and password == "Admin":
                return redirect(url_for('success'))
            else:
                flash("Nieprawidłowy login lub hasło", "error")

        return render_template("login.html")

    def success(self):
        # return render_template("vue_success.html")
        return render_template("success.html")

    def failure(self):
        return render_template("failure.html")