from marshmallow import Schema, fields


class ResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    student_id = fields.Integer(required=True)
    lecture_id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String()
    approved = fields.Boolean(dump_only=True)

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)
