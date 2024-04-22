from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.Lecture import Lecture


class LectureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Lecture
        include_fk = True

