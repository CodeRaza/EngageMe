from app.models import db
import app.config as config
import datetime

class Attendance(db.Model):
    __tablename__ = "attendance"
    __table_args__ = {"schema": config.DB_NAME} 
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey("lecture.id"), nullable=False)
    lecture = db.relationship('Lecture', back_populates='attendance')
