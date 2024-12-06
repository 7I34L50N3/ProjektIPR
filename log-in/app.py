from flask import Flask, render_template, request, redirect, url_for
import hashlib

app = Flask(__name__)

class User:
    def __init__(self, username: str, password: str):
        self._username = None
        self._hashed_password = None

        if username:
            self._username = username

        if password:
            self._hashed_password = hashlib.sha512(password.encode()).hexdigest()

    def login(self, login: str, password: str):
        hash = hashlib.sha512(password.encode())

        if self._username == login and self._hashed_password == hash.hexdigest():
            return True
        else:
            return False

u = User('Admin', 'Admin')

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if u.login(username, password):
            return redirect(url_for('success'))
        else:
            return redirect(url_for('failure'))

    return render_template("login.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/failure")
def failure():
    return render_template("failure.html")

if __name__ == "__main__":
    app.run(debug=True)