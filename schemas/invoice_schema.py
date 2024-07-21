from marshmallow import fields, Schema
from datetime import datetime

def current_time():
    return datetime.now().time()

class PlainInvoiceSchema(Schema):
    id = fields.Int(dump_only=True)
    total_amount = fields.Float(required=True)
    date = fields.DateTime(dump_only=True, default=current_time)
    payment_method = fields.Str(required=True)

class InvoiceUpdateSchema(Schema):
    total_amount = fields.Float()
    payment_method = fields.Str()
    customer_id = fields.Int()
    cashier_id = fields.Int()

class InvoiceSchema(PlainInvoiceSchema):
    customer_id = fields.Int(required=True, load_only=True)
    customer = fields.Method("get_customer", dump_only=True)
    cashier_id = fields.Int(required=True, load_only=True)
    cashier = fields.Method("get_cashier", dump_only=True)

    def get_customer(self, obj):
        from schemas.customer_schema import PlainCustomerSchema
        return PlainCustomerSchema().dump(obj.customer)
    
    def get_cashier(self, obj):
        from schemas.cashier_schema import PlainCashierSchema
        return PlainCashierSchema().dump(obj.cashier)
