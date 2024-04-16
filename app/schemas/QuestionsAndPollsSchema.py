from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.QuestionsAndPolls import QuestionsAndPolls


class QuestionsAndPollsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = QuestionsAndPolls
        include_fk = True

