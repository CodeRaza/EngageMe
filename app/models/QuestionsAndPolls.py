from app.models import db
import app.config as config
import datetime

class QuestionsAndPolls(db.Model):
    __tablename__ = "questions_and_polls"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(
        db.Integer,
        db.ForeignKey("lecture.id"),
        nullable=False
    )
    type = db.Column(db.String(255), nullable=False)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=True, default=None)
    expires_in = db.Column(db.Integer, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.now())
    
    lecture = db.relationship(
        "Lecture", back_populates="questions_and_polls"
    )
    answers_and_votes = db.relationship(
        "AnswersAndVotes", back_populates="question_and_poll"
    )
    