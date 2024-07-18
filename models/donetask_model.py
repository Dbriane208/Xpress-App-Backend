from db import db

class DoneTaskModel(db.Model):
    __tablename__ = "donetasks"

    id = db.Column(db.Integer,primary_key=True)
    carModel = db.Column(db.String(30),unique=False,nullable=False)
    carReg = db.Column(db.String(10),unique=False,nullable=False)
    serviceDone = db.Column(db.String(80),unique=False,nullable=False)
    totalCost = db.Column(db.Float(precision=2),unique=False,nullable=False)
    employee_id = db.Column(db.Integer,db.ForeignKey("employees.id"),unique=False,nullable=False)

    employee = db.relationship("EmployeeModel",back_populates="donetasks")
