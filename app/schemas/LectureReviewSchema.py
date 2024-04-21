from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.LectureReview import LectureReview


class LectureReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LectureReview
        include_fk = True

