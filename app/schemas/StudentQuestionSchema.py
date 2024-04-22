from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.StudentQuestion import StudentQuestion


class StudentQuestionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StudentQuestion
        include_fk = True

