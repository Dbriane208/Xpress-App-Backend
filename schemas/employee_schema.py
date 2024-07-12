from marshmallow import fields,Schema
from schemas import PlainTaskDoneSchema,PlainNewTaskSchema

class PlainEmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class EmployeeUpdateSchema(Schema):
    password = fields.Str()

class EmployeeSchema(PlainEmployeeSchema):
    assigned_tasks = fields.List(fields.Nested(PlainNewTaskSchema(),dump_only=True))
    completed_tasks = fields.List(fields.Nested(PlainTaskDoneSchema(),dump_only=True))    
