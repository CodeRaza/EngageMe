from app.models import db
import app.config as config
import datetime

class AnswersAndVotes(db.Model):
    __tablename__ = "answers_and_votes"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    questions_and_polls_id = db.Column(
        db.Integer,
        db.ForeignKey("questions_and_polls.id"),
        nullable=False
    )
    anonymous = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.now())
    

    question_and_poll = db.relationship(
        "QuestionsAndPolls", back_populates="answers_and_votes"
    )
    