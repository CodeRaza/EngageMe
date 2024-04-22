from app.models import db
import app.config as config
import datetime

classroom_students = db.Table(
    "classroom_students".format(schema=config.DB_NAME),
    db.Model.metadata,
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id"),
    ),
    db.Column(
        "classroom_id",
        db.Integer,
        db.ForeignKey(
            "classroom.id"
        ),
    ),
)

class Classroom(db.Model):
    __tablename__ = "classroom"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    teacher = db.relationship(
        "User", back_populates="teacher_classrooms"
    )
    students = db.relationship(
        "User",
        secondary=classroom_students,
        back_populates="student_classrooms",
    )
    lectures = db.relationship(
        "Lecture", back_populates="classroom", cascade="all, delete-orphan"
    )
