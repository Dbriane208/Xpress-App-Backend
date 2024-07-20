from marshmallow import fields,Schema

class PlainCashierSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class CashierUpdateSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()

class CashierSchema(PlainCashierSchema):
    newtasks = fields.Method("get_newtasks",dump_only=True)

    def get_newtasks(self,obj):
        from schemas.newtask_schema import PlainNewTaskSchema
        return PlainNewTaskSchema(many=True).dump(obj.newtasks)
    
 