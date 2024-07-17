from db import db

class EmployeeModel(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(50),unique=False,nullable=False)

    donetasks = db.relationship("DoneTaskModel",back_populates="employee",lazy="dynamic",cascade="all, delete")
    # newtask = db.relationship("NewTaskModel", back_populates="employee", lazy="dynamic", cascade="all, delete")
