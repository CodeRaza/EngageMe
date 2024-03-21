from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump
from app.models import db
from app.models.TicketDetail import TicketStatus, TicketResolution


class TicketLogsSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    internal_incident_no = fields.String()
    user_id = fields.Integer()
    maintanance_agent = fields.String()
    status = fields.Integer()
    resolution = fields.Integer()
    TDM_no = fields.Integer()
    comments = fields.String()
    timestamp = fields.DateTime("%Y-%m-%d %H:%M:%S")

    @post_dump
    def get_status_andresolution(self, data, **kwargs):

        status = db.session.query(TicketStatus.value).filter(TicketStatus.id == data.get("status")).first()
        resolution = db.session.query(TicketResolution.value).filter(TicketResolution.id == data.get("resolution")).first()
        if status:
            data['status'] = status[0]
        if resolution:
            data['resolution'] = resolution[0]
        return data
        