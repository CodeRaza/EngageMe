from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.AnswersAndVotes import AnswersAndVotes


class AnswersAndVotesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AnswersAndVotes
        include_fk = True

