
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
app = Flask(__name__)

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@127.0.0.1:3307/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicjalizacja SQLAlchemy
db = SQLAlchemy(app)

# Definiowanie modelu
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.username}>'
def test_connection():
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))  # Wykonaj prostą operację SQL
            print("Połączenie z bazą danych działa!")
            return True
        except OperationalError as e:
            print(f"Błąd połączenia z bazą danych: {e}")
            return False


def setup_database():
    with app.app_context():
        # Tworzenie tabel, jeśli nie istnieją
        print("Tworzenie tabel w bazie danych...")
        db.create_all()
        print("Tabele zostały utworzone!")

        # Dodanie użytkownika
        if not User.query.filter_by(username="JohnDoe").first():  # Sprawdzenie, czy użytkownik już istnieje
            print("Dodawanie użytkownika...")
            new_user = User(username='JohnDoe', email='john@example.com')
            db.session.add(new_user)
            db.session.commit()
            print(f"Użytkownik {new_user.username} został dodany!")
        else:
            print("Użytkownik już istnieje.")

# Główna funkcja aplikacji
if __name__ == '__main__':
    if test_connection():
        setup_database()
    app.run(debug=True)

 # with app.app_context():
 #     db.create_all()

# if __name__ == '__main__':
#     app.run(debug=True)

















