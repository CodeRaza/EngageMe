from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.Attendance import Attendance


class AttendanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance
        include_fk = True

attendance_schema = AttendanceSchema()
attendances_schema = AttendanceSchema(many=True)

