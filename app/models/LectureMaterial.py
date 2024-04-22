from app.models import db
import app.config as config
import datetime

class LectureMaterial(db.Model):
    __tablename__ = "lecture_material"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(
        db.Integer,
        db.ForeignKey("lecture.id"),
        nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.now())

    lecture = db.relationship(
        "Lecture", back_populates="materials"
    )
    