from marshmallow import fields, Schema

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
    bookings = fields.Method("get_bookings", dump_only=True)
    invoices = fields.Method("get_invoices", dump_only=True)

    def get_bookings(self, obj):
        from schemas.booking_schema import PlainBookingSchema
        return PlainBookingSchema(many=True).dump(obj.bookings)
    
    def get_invoices(self, obj):
        from schemas.invoice_schema import PlainInvoiceSchema
        return PlainInvoiceSchema(many=True).dump(obj.invoices)
