from db import db

class CustomerModel(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=False,nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    phone = db.Column(db.String(13),unique=True,nullable=False)
    password = db.Column(db.String(50),unique=False,nullable=False)

    bookings = db.relationship("BookingModel",back_populates="customer",lazy="dynamic",cascade="all, delete")
    invoices = db.relationship("InvoiceModel",back_populates="customer",lazy="dynamic",cascade="all, delete")
    