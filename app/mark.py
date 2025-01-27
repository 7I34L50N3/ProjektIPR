from globals import app, db


class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    value = db.Column(db.Float,nullable=False)
    description = db.Column(db.String(255),nullable=True)

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    student = db.relationship('Student', back_populates='marks')
    group = db.relationship('Group', back_populates='marks')

    def check_info_mark(self):
        return {
            "student_id": self.student_id,
            "value": self.value,
            "description": self.description
        }

    def __repr__(self):
        return f"<Mark(value={self.value}, description='{self.description}')>"