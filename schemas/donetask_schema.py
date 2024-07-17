from marshmallow import fields, Schema
from datetime import datetime

def current_time():
    return datetime.now().time()

class PlainTaskDoneSchema(Schema):
    id = fields.Int(dump_only=True)
    carModel = fields.Str(required=True)
    carReg = fields.Str(required=True)
    serviceDone = fields.Str(required=True)
    totalCost = fields.Float(required=True)
    time = fields.Time(dump_only=True, default=current_time)

class TaskDoneUpdateSchema(Schema):
    carModel = fields.Str()
    carReg = fields.Str()
    serviceDone = fields.Str()
    totalCost = fields.Float() 
    employee_id = fields.Int()
    task_id = fields.Int()   

class TaskDoneSchema(PlainTaskDoneSchema):
    employee_id = fields.Int(required=True, load_only=True)
    employee = fields.Method("get_employee", dump_only=True)
    task_id = fields.Int(required=True, load_only=True)
    task = fields.Method("get_task", dump_only=True)

    def get_employee(self, obj):
        from schemas import PlainEmployeeSchema
        return PlainEmployeeSchema().dump(obj.employee)

    def get_task(self, obj):
        from schemas import PlainNewTaskSchema
        return PlainNewTaskSchema().dump(obj.task)