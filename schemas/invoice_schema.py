from marshmallow import fields,Schema
from schemas import PlainCustomerSchema
from datetime import datetime

def current_time():
    return datetime.now(datetime.UTC)

class PlainInvoiceSchema(Schema):
    id = fields.Int(dump_only=True)
    total_amount = fields.Float(required=True)
    date = fields.DateTime(dump_only=True,default=current_time)
    payment_method = fields.Str(required=True)

class InvoiceUpdateSchema(Schema):
    total_amount = fields.Float()
    payment_method = fields.Str()
    customer_id = fields.Int()

class InvoiceSchema(PlainInvoiceSchema):
    customer_id = fields.Int(required=True,load_only=True)
    customer = fields.Nested(PlainCustomerSchema(),dump_only=True)