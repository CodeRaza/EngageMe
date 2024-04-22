from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.QuestionsAndPolls import QuestionsAndPolls
from app.schemas.AnswersAndVotesSchema import AnswersAndVotesSchema

class QuestionsAndPollsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = QuestionsAndPolls
        include_fk = True
    answers_and_votes = fields.Nested(AnswersAndVotesSchema, many=True)

