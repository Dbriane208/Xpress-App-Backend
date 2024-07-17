from db import db

class BookingModel(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer,primary_key=True)
    service = db.Column(db.String(80),unique=False,nullable=False)
    branch = db.Column(db.String(80),unique=False,nullable=False)
    username = db.Column(db.String(80),unique=False,nullable=False)
    phone = db.Column(db.String(13),unique=False,nullable=False)
    time = db.Column(db.Time,unique=False,nullable=False)
    date = db.Column(db.Date,unique=False,nullable=False)
    carReg = db.Column(db.String(10),unique=False,nullable=False)
    carModel = db.Column(db.String(20),unique=False,nullable=False)
    customer_id = db.Column(db.Integer,db.ForeignKey("customers.id"),unique=False,nullable=False)

    customer = db.relationship("CustomerModel",back_populates="bookings")