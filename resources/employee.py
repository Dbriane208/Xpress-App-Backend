from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import EmployeeModel
from schemas import EmployeeSchema, EmployeeUpdateSchema

blp = Blueprint("Employees","employees",description="Operations on employees")

@blp.route("/employee/<int:employee_id>")
class Employee(MethodView):
    @blp.response(200,EmployeeSchema)
    def get(self,employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)
        return employee
    
    def delete(self,employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)

        db.session.delete(employee)
        db.session.commit()

        return {"message":"Employee deleted successfully"}
    
    @blp.arguments(EmployeeUpdateSchema)
    @blp.response(200,EmployeeSchema)
    def put(self,employee_data,employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)

        for key, value in employee_data.items():
            setattr(employee, key, value)

        db.session.commit()

        return employee

@blp.route("/employee")     
class EmployeeList(MethodView):
    @blp.response(200,EmployeeSchema(many=True))
    def get(self):
        return EmployeeModel.query.all()    
    
    @blp.arguments(EmployeeSchema)
    @blp.response(201,EmployeeSchema)
    def post(self,employee_data):

        existing_employee = EmployeeModel.query.filter_by(email=employee_data['email']).first()

        if existing_employee:
            abort(400, message="An employee with this email already exists")
        
        employee = EmployeeModel(**employee_data)

        try:
            db.session.add(employee)
            db.session.commit()

        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred creating a new employee"
            )     

        return employee     