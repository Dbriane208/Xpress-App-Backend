from marshmallow import fields, Schema
from datetime import datetime

def current_time():
    return datetime.now().time()

class PlainTaskDoneSchema(Schema):
    id = fields.Int(dump_only=True)
    employee_name = fields.Str(required=True)
    car_model = fields.Str(required=True)
    car_reg = fields.Str(required=True)
    service_done = fields.Str(required=True)
    total_cost = fields.Float(required=True)
    time = fields.Time(dump_only=True, default=current_time)

class TaskDoneUpdateSchema(Schema):
    employee_name = fields.Str()
    car_model = fields.Str()
    car_reg = fields.Str()
    service_done = fields.Str()
    total_cost = fields.Float() 
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

class PlainNewTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    employee_name = fields.Str(required=True)
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
    employee_id = fields.Int(required=True, load_only=True)
    employee = fields.Method("get_employee", dump_only=True)
    cashier_id = fields.Int(required=True, load_only=True)
    cashier = fields.Method("get_cashier", dump_only=True)

    def get_employee(self, obj):
        from schemas import PlainEmployeeSchema
        return PlainEmployeeSchema().dump(obj.employee)

    def get_cashier(self, obj):
        from schemas import PlainCashierSchema
        return PlainCashierSchema().dump(obj.cashier)
