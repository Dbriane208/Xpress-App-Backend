from db import db

class NewTaskModel(db.Model):
    __tablename__ = "newtasks"

    id = db.Column(db.Integer,primary_key=True)
    employeeName = db.Column(db.String(80),unique=False,nullable=False)
    carModel = db.Column(db.String(80),unique=False,nullable=False)
    carReg = db.Column(db.String(80),unique=False,nullable=False)
    serviceDone = db.Column(db.String(80),unique=False,nullable=False)
    employee_id = db.Column(db.Integer,db.ForeignKey("employees.id"),unique=False,nullable=False)

    employee = db.relationship("EmployeeModel",back_populates="newtask")