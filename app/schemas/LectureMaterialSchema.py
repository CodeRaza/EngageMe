from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.LectureMaterial import LectureMaterial


class LectureMaterialSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LectureMaterial

