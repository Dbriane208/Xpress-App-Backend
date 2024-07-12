from marshmallow import fields,Schema
from schemas import PlainBookingSchema,PlainInvoiceSchema

class PlainCustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True)

class CustomerUpdateSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    password = fields.Str()

class CustomerSchema(PlainCustomerSchema):
    bookings = fields.List(fields.Nested(PlainBookingSchema(),dump_only=True)) 
    invoice = fields.Nested(PlainInvoiceSchema(),dump_only=True)  
    