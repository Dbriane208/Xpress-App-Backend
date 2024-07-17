from marshmallow import fields, Schema
from schemas.donetask_schema import TaskDoneSchema

class PlainEmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class EmployeeUpdateSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()

class EmployeeSchema(PlainEmployeeSchema):
    donetasks = fields.List(fields.Nested(TaskDoneSchema(),dump_only=True))