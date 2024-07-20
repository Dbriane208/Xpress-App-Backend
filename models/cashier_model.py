from db import db

class CashierModel(db.Model):
    __tablename__ = "cashiers"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=False,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),unique=False,nullable=False)

    newtasks = db.relationship("NewTaskModel",back_populates="cashier",lazy="dynamic",cascade="all, delete")