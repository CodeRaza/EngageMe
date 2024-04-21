from app.models import db
import app.config as config
import jwt
from datetime import datetime,timedelta,timezone
from app.models.Classroom import classroom_students

class User(db.Model):
    __tablename__ = "user"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    
    teacher_classrooms = db.relationship(
        "Classroom",
        back_populates="teacher",
    )
    student_classrooms = db.relationship(
        "Classroom",
        secondary=classroom_students,
        back_populates="students"
    )
    answers_and_votes = db.relationship(
        "AnswersAndVotes",
        back_populates="student"
    )
    lecture_reviews = db.relationship(
        "LectureReview", back_populates="student"
    )
    student_questions = db.relationship(
        "StudentQuestion", back_populates="student"
    )
    moderations_as_teacher = db.relationship(
        "Moderation",
        back_populates="teacher",
        foreign_keys="[Moderation.teacher_id]"
    )
    moderations_as_student = db.relationship(
        "Moderation",
        back_populates="student",
        foreign_keys="[Moderation.student_id]"
    )

    @property
    def rolenames(self):
        try:
            return self.role.split(",")
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(email=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def get_reset_token(self, expires=500):
        return jwt.encode( {
                            'reset_password': self.email,
                            'exp': datetime.now(tz=timezone.utc)+timedelta(seconds=500)
                        },
                        config.MAIL_SECRET_KEY,
                        "HS256"
                    )

    @property
    def identity(self):
        return self.id
