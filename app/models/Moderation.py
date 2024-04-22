from app.models import db
import app.config as config
import jwt
from datetime import datetime,timedelta,timezone
from app.models.Classroom import classroom_students

class Moderation(db.Model):
    __tablename__ = "moderation"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    blocked = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(255), unique=True)
    warnings = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Relationships
    teacher = db.relationship("User", back_populates="moderations_as_teacher", foreign_keys=[teacher_id])
    student = db.relationship("User", back_populates="moderations_as_student", foreign_keys=[student_id])
