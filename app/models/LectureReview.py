from app.models import db
import app.config as config
import datetime

class LectureReview(db.Model):
    __tablename__ = "lecture_review"
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
    favorite_checked = db.Column(db.Boolean, nullable=True, default=False)
    thumbsup_checked = db.Column(db.Boolean, nullable=True, default=False)
    thumbsdown_checked = db.Column(db.Boolean, nullable=True, default=False)
    confuse_checked = db.Column(db.Boolean, nullable=True, default=False)
    cannot_hear_checked = db.Column(db.Boolean, nullable=True, default=False)
    cannot_see_checked = db.Column(db.Boolean, nullable=True, default=False)
    cannot_see_button_checked = db.Column(db.Boolean, nullable=True, default=False)
    cannot_hear_button_checked = db.Column(db.Boolean, nullable=True, default=False)
    needtorepeat_button_checked = db.Column(db.Boolean, nullable=True, default=False)
    rate_content = db.Column(db.String(255), nullable=True, default=None)
    effectively_communicate = db.Column(db.String(255), nullable=True, default=None)
    examples_clear = db.Column(db.String(255), nullable=True, default=None)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    lecture = db.relationship(
        "Lecture", back_populates="lecture_reviews"
    )
    student = db.relationship(
        "User", back_populates="lecture_reviews"
    )


