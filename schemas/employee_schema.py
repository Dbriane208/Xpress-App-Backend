from marshmallow import fields, Schema

class PlainEmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class EmployeeUpdateSchema(Schema):
    password = fields.Str()

class EmployeeSchema(PlainEmployeeSchema):
    assigned_tasks = fields.Method("get_assigned_tasks", dump_only=True)
    completed_tasks = fields.Method("get_completed_tasks", dump_only=True)

    def get_assigned_tasks(self, obj):
        from schemas.tasks_schema import PlainNewTaskSchema
        return PlainNewTaskSchema(many=True).dump(obj.assigned_tasks)

    def get_completed_tasks(self, obj):
        from schemas.tasks_schema import PlainTaskDoneSchema
        return PlainTaskDoneSchema(many=True).dump(obj.completed_tasks)
