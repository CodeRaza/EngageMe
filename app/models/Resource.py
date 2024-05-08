from app.models import db
import app.config as config


class Resource(db.Model):
    __tableargs__ = {"schema": config.DB_NAME}
    __tablename__ = "resource"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey("lecture.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    approved = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='shared_resources', overlaps="student")
    student = db.relationship("User", back_populates="shared_resources")
    lecture = db.relationship("Lecture", back_populates="shared_resources")
