from db import db

class DoneTaskModel(db.Model):
    __tablename__ = "donetasks"

    id = db.Column(db.Integer,primary_key=True)
    carModel = db.Column(db.String(30),nullable=False)
    carReg = db.Column(db.String(10),nullable=False)
    serviceDone = db.Column(db.String(80),nullable=False)
    totalCost = db.Column(db.Float(precision=2),nullable=False)
    employee_id = db.Column(db.Integer,db.ForeignKey("employees.id"),unique=False,nullable=False)
    task_id =  db.Column(db.Integer,db.ForeignKey("newtasks.id"),unique=False,nullable=False)

    employee = db.relationship("EmployeeModel",back_populates="donetasks")
