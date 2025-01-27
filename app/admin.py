from user import User,UserRepo
from group import GroupRepo
from globals import db,app

class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',  # Wartość dla klasy Admin
    }
    user_repo = UserRepo()
    group_repo = GroupRepo()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)  # Wywołanie konstruktora User

    # Dodawanie nowego użytkownika
    def add_user(self, username, password, email, name, surname, role="user"):
        try:
            user = self.user_repo.create(username, password, email, name, surname, role)
            return user
        except ValueError as e:
            print(f"Błąd: {e}")

    # Edycja istniejącego użytkownika
    def edit_user(self, user_id, **kwargs):
        user = self.user_repo.update(user_id, **kwargs)
        if user:
            return user

    # Dodawanie nowej grupy
    def add_group(self, name, description=None):
        try:
            group = self.group_repo.create(name, description)
            return group
        except:
            return None

    # Edycja istniejącej grupy
    def edit_group(self, group_id, **kwargs):
        group = self.group_repo.update(group_id, **kwargs)
        if group:
            return group