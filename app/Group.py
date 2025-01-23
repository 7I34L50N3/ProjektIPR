
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

#grupa
class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Group {self.name}>"

# Funkcja testująca połączenie z bazą danych
def test_connection():
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))  # Wykonaj prostą operację SQL
            print("Połączenie z bazą danych działa!")
            return True
        except OperationalError as e:
            print(f"Błąd połączenia z bazą danych: {e}")
            return False

# Repozytorium grup
class GroupRepo:
    def __init__(self):
        pass

    def create(self, name, description=None):
        new_group = Group(name=name, description=description)
        db.session.add(new_group)
        db.session.commit()
        return new_group

    def update(self, group_id, name=None, description=None):
        group = Group.query.get(group_id)
        if group:
            if name:
                group.name = name
            if description:
                group.description = description
            db.session.commit()
        return group

    def find_by_argument(self, **kwargs):
        return Group.query.filter_by(**kwargs).all()

    def delete(self, group_id):
        group = Group.query.get(group_id)
        if group:
            db.session.delete(group)
            db.session.commit()
        return group

    def find(self):
        #zwraca wszystkie grupy
        return Group.query.all()

# Tworzenie tabel i dodawanie przykładowej grupy
with app.app_context():
    db.create_all()

    # Tworzenie instancji repozytorium
    repo = GroupRepo()

    # Dodanie przykładowej grupy
    print("Dodawanie przykładowej grupy...")
    example_group = repo.create(name="Beginner English", description="Grupa dla początkujących")
    print(f"Utworzono grupę: {example_group}")

    # Wyświetlenie wszystkich grup
    print("Wszystkie grupy w bazie:")
    groups = repo.find()
    for group in groups:
        print(group)

# Główna funkcja
if __name__ == '__main__':
    if test_connection():
        app.run(debug=True)



# # Definiowanie modelu
# class User(db.odeMl):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), nullable=False, unique=True)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#
#     def __repr__(self):
#         return f'<User {self.username}>'
# def test_connection():
#     with app.app_context():
#         try:
#             db.session.execute(text('SELECT 1'))  # Wykonaj prostą operację SQL
#             print("Połączenie z bazą danych działa!")
#             return True
#         except OperationalError as e:
#             print(f"Błąd połączenia z bazą danych: {e}")
#             return False
#
#
# def setup_database():
#     with app.app_context():
#         # Tworzenie tabel, jeśli nie istnieją
#         print("Tworzenie tabel w bazie danych...")
#         db.create_all()
#         print("Tabele zostały utworzone!")
#
#         # Dodanie użytkownika
#         if not User.query.filter_by(username="JohnDoe").first():  # Sprawdzenie, czy użytkownik już istnieje
#             print("Dodawanie użytkownika...")
#             new_user = User(username='JohnDoe', email='john@example.com')
#             db.session.add(new_user)
#             db.session.commit()
#             print(f"Użytkownik {new_user.username} został dodany!")
#         else:
#             print("Użytkownik już istnieje.")
#
# # Główna funkcja aplikacji
# if __name__ == '__main__':
#     if test_connection():
#         setup_database()
#     app.run(debug=True)

















