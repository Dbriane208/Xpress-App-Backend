from marshmallow import Schema,fields
from schemas import PlainCustomerSchema

class PlainBookingSchema(Schema):
    id = fields.Int(dump_only=True)
    service = fields.Str(required=True)
    branch = fields.Str(required=True)
    username = fields.Str(required=True)
    phone = fields.Str(required=True)
    time = fields.Time(required=True)
    date = fields.Date(required=True)
    carReg = fields.Str(required=True)
    carModel = fields.Str(required=True)

class BookingSchemaUpdate(Schema):
    service = fields.Str()
    branch = fields.Str()
    username = fields.Str()
    phone = fields.Str()
    time = fields.Time()
    date = fields.Date()
    carReg = fields.Str()
    carModel = fields.Str()
    customer_id = fields.Int()
    
class BookingSchema(PlainBookingSchema):
    customer_id = fields.Int(required=True,load_only=True)
    customer = fields.Nested(PlainCustomerSchema(),dump_only=True)