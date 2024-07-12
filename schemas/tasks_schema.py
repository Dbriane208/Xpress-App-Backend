from marshmallow import fields,Schema
from schemas import PlainEmployeeSchema,PlainNewTaskSchema,PlainCashierSchema
from datetime import datetime

def current_time():
    return datetime.now(datetime.UTC)

class PlainTaskDoneSchema(Schema):
    id = fields.Int(dump_only=True)
    employee_name = fields.Str(required=True)
    car_model = fields.Str(required=True)
    car_reg = fields.Str(required=True)
    service_done = fields.Str(required=True)
    total_cost = fields.Float(required=True)
    time = fields.Time(dump_only=True,default=current_time)

class TaskDoneUpdate(Schema):
    employee_name = fields.Str()
    car_model = fields.Str()
    car_reg = fields.Str()
    service_done = fields.Str()
    total_cost = fields.Float() 
    employee_id = fields.Int()
    task_id = fields.Int()   

class TaskDoneSchema(PlainTaskDoneSchema):
    employee_id = fields.Int(required=True,load_only=True)
    employee = fields.Nested(PlainEmployeeSchema(),dump_only=True)
    task_id = fields.Int(required=True,load_only=True)
    task = fields.Nested(PlainNewTaskSchema(),dump_only=True)

class PlainNewTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    emplyoee_name = fields.Str(required=True)
    car_model = fields.Str(required=True)
    car_reg = fields.Str(required=True)
    service_done = fields.Str(required=True)

class NewTaskUpdateSchema(Schema):
    employee_name = fields.Str()
    car_model = fields.Str()
    car_reg = fields.Str()
    service_done = fields.Str()
    employee_id = fields.Int()
    cashier_id = fields.Int()

class NewTaskSchema(PlainNewTaskSchema):
    employee_id = fields.Int(required=True,load_only=True)
    employee = fields.Nested(PlainEmployeeSchema(),dump_only=True)
    cashier_id = fields.Int(required=True,load_only=True)
    cashier = fields.Nested(PlainCashierSchema(),dump_only=True)