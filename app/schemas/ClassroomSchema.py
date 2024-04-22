from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump, validate
from datetime import datetime, timedelta
from app.models.Classroom import Classroom


class ClassroomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Classroom
        include_fk = True


# class EditTicketSchema(SQLAlchemyAutoSchema):
#     source_incident_no = fields.String()
#     reporting_source_id = fields.Integer()
#     internal_incident_no = fields.String(required=True, allow_none=False)
#     status_id = fields.Integer()
#     opening_time = fields.DateTime()
#     source_time = fields.DateTime()
#     phase_id = fields.Integer()
#     network_no = fields.String()
#     site = fields.String()
#     element_type_id = fields.Integer()
#     element_id = fields.Integer()
#     device_type_id = fields.Integer()
#     last_octet = fields.String()
#     fault_description_id = fields.Integer()
#     resolution_id = fields.Integer()
#     TDM_no = fields.Integer()
#     closing_time = fields.DateTime()
#     maintanance_agent = fields.String()
#     comments = fields.String(allow_none=True)


# class GetTicketSchema(SQLAlchemyAutoSchema):
#     source_incident_no = fields.String()
#     reporting_source_id = fields.Integer()
#     internal_incident_no = fields.String()
#     status_id = fields.Integer()
#     opening_time = fields.DateTime("%Y-%m-%d %H:%M:%S")
#     source_time = fields.DateTime("%Y-%m-%d %H:%M:%S")
#     phase_id = fields.Integer()
#     network_no = fields.String()
#     site = fields.String()
#     element_type_id = fields.Integer()
#     element_id = fields.String()
#     device_type_id = fields.String()
#     last_octet = fields.String()
#     fault_description_id = fields.Integer()
#     resolution_id = fields.Integer()
#     closing_time = fields.DateTime("%Y-%m-%d %H:%M:%S")
#     comments = fields.String()
#     status = fields.Pluck(TicketStatusSchema, "value")
#     fault_description = fields.Pluck(FaultDescriptionSchema, "value")
#     resolution = fields.Pluck(TicketResolutionSchema, "value")
#     device_type = fields.Nested(
#         SLASSchema(only=("device_type", "time_to_respond", "time_to_resolve"))
#     )

#     @post_dump
#     def get_sla_info(self, data, **kwargs):
#         """
#         Calculate SLA related fields for each Ticket
#         """
#         if data.get("device_type"):
#             data["time_to_respond"] = int(data["device_type"]["time_to_respond"])
#             data["time_to_resolve"] = int(data["device_type"]["time_to_resolve"])
#             # calculate Resolution SLA
#             if data["opening_time"]:
#                 opening_time = datetime.strptime(
#                     data["opening_time"], "%Y-%m-%d %H:%M:%S"
#                 )
#                 resolve_sla_breach_time = opening_time + timedelta(
#                     hours=data["time_to_resolve"]
#                 )
#                 data["time_to_resolve"] = resolve_sla_breach_time.strftime(
#                     "%Y-%m-%d %H:%M:%S"
#                 )
#                 now = datetime.now()
#                 hour_before_response_sla = resolve_sla_breach_time - timedelta(hours=1)
#                 if resolve_sla_breach_time < now:
#                     if data["status"] == 8:
#                         closing_time = datetime.strptime(
#                             data["closing_time"], "%Y-%m-%d %H:%M:%S"
#                         )
#                         if resolve_sla_breach_time > closing_time:
#                             data["time_to_resolve_sla"] = "green"
#                         else:
#                             data["time_to_resolve_sla"] = "red"
#                     else:
#                         data["time_to_resolve_sla"] = "red"
#                 else:
#                     if hour_before_response_sla < now:
#                         if data["status"] == 8:
#                             closing_time = datetime.strptime(
#                                 data["closing_time"], "%Y-%m-%d %H:%M:%S"
#                             )
#                             if resolve_sla_breach_time > closing_time:
#                                 data["time_to_resolve_sla"] = "green"
#                             else:
#                                 data["time_to_resolve_sla"] = "yellow"
#                         else:
#                             data["time_to_resolve_sla"] = "yellow"
#                     else:
#                         data["time_to_resolve_sla"] = "green"

#                 # calculate Response SLA
#                 respond_sla_breach_time = opening_time + timedelta(minutes=15)
#                 data["time_to_respond"] = str(data["time_to_respond"]) + " Minutes"

#                 if data["status_id"] == 1:
#                     if respond_sla_breach_time < now:
#                         data["time_to_respond_sla"] = "red"
#                     else:
#                         data["time_to_respond_sla"] = "green"
#                 else:
#                     in_process_time = db.session.query(TicketLogs.timestamp).filter(
#                         and_(
#                             TicketLogs.status == 2,
#                             TicketLogs.internal_incident_no
#                             == data["internal_incident_no"],
#                         )
#                     ).first()
#                     if in_process_time:
#                         if respond_sla_breach_time < in_process_time[0]:
#                             data["time_to_respond_sla"] = "red"
#                         else:
#                             data["time_to_respond_sla"] = "green"

#         return data


# class TicketReportSchema(SQLAlchemyAutoSchema):
#     source_incident_no = fields.String(required=True, allow_none=False)
#     reporting_source_id = fields.Integer()
#     internal_incident_no = fields.String(required=True, allow_none=False)
#     status_id = fields.Integer()
#     opening_time = fields.DateTime("%Y-%m-%d %H:%M:%S")
#     source_time = fields.DateTime("%Y-%m-%d %H:%M:%S")
#     phase_id = fields.Integer()
#     network_no = fields.String()
#     site = fields.String()
#     element_type_id = fields.Integer()
#     element_id = fields.String()
#     device_type_id = fields.String(required=True, allow_none=False)
#     last_octet = fields.String(required=True, allow_none=False)
#     fault_description_id = fields.Integer()
#     resolution_id = fields.Integer()
#     TDM_no = fields.Integer()
#     closing_time = fields.DateTime("%Y-%m-%d %H:%M:%S")
#     maintanance_agent = fields.String()
#     comments = fields.String()
#     status = fields.Pluck(TicketStatusSchema, "value")
#     reporting_source = fields.Pluck(ReportingSourceSchema, "value")
#     fault_description = fields.Pluck(FaultDescriptionSchema, "value")
#     resolution = fields.Pluck(TicketResolutionSchema, "value")
#     phase = fields.Pluck(PhaseSchema, "value")
#     element_type = fields.Pluck(ElementTypeSchema, "value")
#     device_type = fields.Nested(
#         SLASSchema(only=("device_type", "time_to_respond", "time_to_resolve"))
    # )
