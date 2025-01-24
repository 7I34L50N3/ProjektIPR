from user import UserRepo,User
from group import GroupRepo
from globals import db,app

class student(User):
    def check_marks(self):
        pass

    def check_groups(self):
        groups = [group.name for group in self.groups]
        return groups
