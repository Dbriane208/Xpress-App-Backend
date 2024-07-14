from db import db

class InvoiceModel(db.Model):
    __tablename__ = "invoice"

    id = db.Column(db.Integer,primary_key=True)
    total_amount = db.Column(db.Float(precision=2),nullable=False)
    payment_method = db.Column(db.String(10),nullable=False)
    customer_id = db.Column(db.Integer,db.ForeignKey("customers.id"),unique=False,nullable=True)

    customer = db.relationship("CustomerModel",back_populates="invoices")