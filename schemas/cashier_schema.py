from marshmallow import fields,Schema
from schemas import PlainNewTaskSchema

class PlainCashierSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class CashierUpdateSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    new_task_id = fields.Int()

class CashierSchema(PlainCashierSchema):
    new_task_id = fields.Int(required=True,load_only=True)
    tasks = fields.List(fields.Nested(PlainNewTaskSchema(),dump_only=True))