from user import UserRepo,User
from group import GroupRepo
from globals import db,app
from mark import Mark

class Student(User):
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }
    marks = db.relationship('Mark', back_populates='student', lazy='dynamic')
    def check_marks(self):
        return self.marks.all()

    def check_groups(self):
        return self.groups