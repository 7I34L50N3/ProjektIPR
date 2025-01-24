from user import User,UserRepo
from group import GroupRepo
from globals import db,app
class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',  # Wartość dla klasy Admin
    }
    def __init__(self,session,**kwargs):
        super().__init__(**kwargs)  # Wywołanie konstruktora User
        self.user_repo = UserRepo(session)
        self.group_repo = GroupRepo(session)

    # Dodawanie nowego użytkownika
    def add_user(self, username, password, email, name, surname, role="user"):
        try:
            user = self.user_repo.create(username, password, email, name, surname, role)
            print(f"Użytkownik {username} został pomyślnie dodany.")
            return user
        except ValueError as e:
            print(f"Błąd: {e}")

    # Edycja istniejącego użytkownika
    def edit_user(self, user_id, **kwargs):
        user = self.user_repo.update(user_id, **kwargs)
        if user:
            print(f"Użytkownik {user.username} został zaktualizowany.")
            return user
        else:
            print(f"Nie znaleziono użytkownika o ID {user_id}.")

    # Dodawanie nowej grupy
    def add_group(self, name, description=None):
        try:
            group = self.group_repo.create(name, description)
            print(f"Grupa {name} została pomyślnie dodana.")
            return group
        except ValueError as e:
            print(f"Błąd: {e}")

    # Edycja istniejącej grupy
    def edit_group(self, group_id, **kwargs):
        group = self.group_repo.update(group_id, **kwargs)
        if group:
            print(f"Grupa {group.name} została zaktualizowana.")
            return group
        else:
            print(f"Nie znaleziono grupy o ID {group_id}.")

    # Sprawdzenie grup
    def check_groups(self):
        groups = self.group_repo.find()
        if groups:
            print("Lista grup:")
            for group in groups:
                print(f"- {group.name}: {group.description}")
        else:
            print("Brak grup w systemie.")

    # Sprawdzenie użytkowników
    def check_users(self):
        users = self.user_repo.find()
        if users:
            print("Lista użytkowników:")
            for user in users:
                print(f"- {user.username} ({user.role}): {user.email}")
        else:
            print("Brak użytkowników w systemie.")

if __name__ == "__main__":
    with app.app_context():
        admin= Admin(db.session)

        admin.add_user(
            username="franekthebuilder",
            password="12345",
            email="franek@destroyer.com",
            name="franek",
            surname="żyd3",
            role="student"
        )