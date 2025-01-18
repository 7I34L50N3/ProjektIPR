from flask import Flask, render_template, request, redirect, url_for
from user import UserRepo
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Poprawna konfiguracja połączenia z MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER', 'user')}:{os.getenv('DB_PASSWORD', 'password')}"
    f"@{os.getenv('DB_HOST', 'db')}:3306/{os.getenv('DB_NAME', 'app_db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

u = UserRepo('Admin', 'Admin')

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#
#     def __repr__(self):
#         return f'<User {self.username}>'

def create_tables():
    db.create_all()

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

@app.route('/add_user/<username>')
def add_user(username):
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return f"Użytkownik {username} został dodany do bazy danych!"

if __name__ == "__main__":
    create_tables()
    app.run(host='0.0.0.0', port=5000)
