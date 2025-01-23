from flask import Flask, render_template, request, redirect, url_for, flash, session

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
        app.secret_key = "secret_key"  # Klucz do obsługi sesji
        app.add_url_rule('/', 'login', self.login, methods=['GET', 'POST'])
        app.add_url_rule('/success', 'success', self.success, methods=['GET'])
        app.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])

    def login(self):
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            print(f'Username: {username} | Password: {password}')

            # Weryfikacja użytkownika (przykład hardkodowany, zastąp bazą danych)
            if username == "Admin" and password == "Admin":
                session['user_id'] = username  # Przechowuj nazwę użytkownika w sesji
                return redirect(url_for('success'))
            else:
                flash("Nieprawidłowy login lub hasło", "error")

        return render_template("login.html")

    def success(self):
        user_id = session.get('user_id')  # Pobierz ID użytkownika z sesji
        if not user_id:
            flash("Musisz być zalogowany, aby uzyskać dostęp do tej strony.", "error")
            return redirect(url_for('login'))

        return render_template("success.html", username=user_id)

    def logout(self):
        session.pop('user_id', None)  # Usuń użytkownika z sesji
        flash("Zostałeś wylogowany.", "info")
        return redirect(url_for('login'))




class AdminApi:
    def __init__(self):
        self.name = "AdminAPI"

    def register_routes(self, app):
        app.add_url_rule('/dashboard', 'admin_dashboard', self.admin_dashboard, methods=['GET'])

    def admin_dashboard(self):
        return render_template("success.html")