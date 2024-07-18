from marshmallow import fields, Schema

class PlainNewTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    carModel = fields.Str(required=True)
    carReg = fields.Str(required=True)
    serviceDone = fields.Str(required=True)

class NewTaskUpdateSchema(Schema):
    carModel = fields.Str()
    carReg = fields.Str()
    serviceDone = fields.Str()
    employee_id = fields.Int()

class NewTaskSchema(PlainNewTaskSchema):
    employee_id = fields.Int(required=True, load_only=True)
    employee = fields.Method("get_employee", dump_only=True)

    def get_employee(self, obj):
        from schemas import PlainEmployeeSchema
        return PlainEmployeeSchema().dump(obj.employee)
