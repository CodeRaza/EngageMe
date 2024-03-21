from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class ReportingSourceSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    value = fields.String()

class TicketStatusSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    value = fields.String()

class SLASSchema(SQLAlchemyAutoSchema):
    device_type = fields.String()
    time_to_respond = fields.String()
    time_to_resolve = fields.String()

class FaultDescriptionSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    value = fields.String()

class TicketResolutionSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    value = fields.String()

class PhaseSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    value = fields.String()

class ElementTypeSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    value = fields.String()