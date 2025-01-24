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

if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        # student = Student.query.filter_by(username="Janekthebuilder").first()
        # group_repo = GroupRepo()
        # group = group_repo.find_by_argument(name="Beginner English")
        # # Dodaj nową ocenę
        # mark1 = Mark(value=4.5, description="Egzamin końcowy", student=student, group=group)
        # mark2 = Mark(value=5.0, description="Sprawdzian z algebry", student=student, group=group)
        # db.session.add(mark1)
        # db.session.add(mark2)
        # db.session.commit()
        #
        # print(f"Oceny zostały dodane dla studenta {student.name} {student.surname}.")
        #
        # # Wyświetl wszystkie oceny studenta
        # print("Oceny:")
        # for mark in student.check_marks():
        #     print(f"- {mark.value}: {mark.description}")


        user_repo = UserRepo()  # Singleton
        user1 = user_repo.find_by_argument(username="Janekthebuilder")
        user1.change_password(db.session, "123")
        db.session.commit()
