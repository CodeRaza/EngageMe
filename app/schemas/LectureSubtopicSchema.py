from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.LectureSubtopic import LectureSubtopic


class LectureSubtopicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LectureSubtopic

