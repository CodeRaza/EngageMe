from app.models import db
import app.config as config
import datetime

class Lecture(db.Model):
    __tablename__ = "lecture"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(
        db.Integer,
        db.ForeignKey("classroom.id"),
        nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    live = db.Column(db.Boolean, nullable=True, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    classroom = db.relationship(
        "Classroom", back_populates="lectures"
    )
    materials = db.relationship(
        "LectureMaterial", back_populates="lecture", cascade="all, delete-orphan"
    )
    subtopics = db.relationship(
        "LectureSubtopic", back_populates="lecture", cascade="all, delete-orphan"
    )
    questions_and_polls = db.relationship(
        "QuestionsAndPolls", back_populates="lecture", cascade="all, delete-orphan"
    )
    lecture_reviews = db.relationship(
        "LectureReview", back_populates="lecture", cascade="all, delete-orphan"
    )
    student_questions = db.relationship(
        "StudentQuestion", back_populates="lecture", cascade="all, delete-orphan"
    )


