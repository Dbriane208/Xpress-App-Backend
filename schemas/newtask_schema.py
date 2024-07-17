from marshmallow import fields, Schema

class PlainNewTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    employeeName = fields.Str(required=True)
    carModel = fields.Str(required=True)
    car_reg = fields.Str(required=True)
    service_done = fields.Str(required=True)

class NewTaskUpdateSchema(Schema):
    employeeName = fields.Str()
    carModel = fields.Str()
    carReg = fields.Str()
    serviceDone = fields.Str()
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
