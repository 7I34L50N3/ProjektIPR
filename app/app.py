from flask import Flask, render_template, request, redirect, url_for
from user import User

app = Flask(__name__)

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
    return render_template("vue_success.html")

@app.route("/failure")
def failure():
    return render_template("failure.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)