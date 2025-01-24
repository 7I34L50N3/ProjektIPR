from user import UserRepo,User
from group import GroupRepo
from globals import db,app

class Student(User):
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }
    def check_marks(self):
        pass

    def check_groups(self):
        return self.groups
