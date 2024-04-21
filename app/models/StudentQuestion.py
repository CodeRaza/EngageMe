from app.models import db
import app.config as config
import datetime

class StudentQuestion(db.Model):
    __tablename__ = "student_question"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(
        db.Integer,
        db.ForeignKey("lecture.id"),
        nullable=False
    )
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    question = db.Column(db.Text, nullable=False)
    anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    lecture = db.relationship(
        "Lecture", back_populates="student_questions"
    )
    student = db.relationship(
        "User", back_populates="student_questions"
    )


