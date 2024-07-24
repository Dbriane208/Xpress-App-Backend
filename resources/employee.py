from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from blocklist import BLOCKLIST
from models import EmployeeModel
from schemas import EmployeeSchema, EmployeeUpdateSchema, EmployeeLoginSchema, PlainTaskDoneSchema,PlainNewTaskSchema

blp = Blueprint("Employees","employees",description="Operations on employees")

@blp.route("/employee/<int:employee_id>")
class Employee(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200,EmployeeSchema)
    def get(self,employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)
        return employee
    
    @jwt_required(refresh=True)
    def delete(self,employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)

        db.session.delete(employee)
        db.session.commit()

        return {"message":"Employee deleted successfully"}
    
    @jwt_required(refresh=True)
    @blp.arguments(EmployeeUpdateSchema)
    @blp.response(200,EmployeeSchema)
    def put(self,employee_data,employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)

        for key, value in employee_data.items():
            setattr(employee, key, value)

        db.session.commit()

        return employee
    
@blp.route("/employee/login")
class EmployeeLogin(MethodView):
    @blp.arguments(EmployeeLoginSchema)
    @jwt_required(fresh=True)
    def post(self,employee_data):
        employee = EmployeeModel.query.filter(
            EmployeeModel.email == employee_data["email"]
        ).first()

        if employee and pbkdf2_sha256.verify(employee_data["password"],employee.password):
            access_token = create_access_token(identity=employee.id,fresh=True)
            refresh_token = create_refresh_token(identity=employee.id)
            employee_data = EmployeeSchema().dump(employee)
            employee_data['access_token'] = access_token
            employee_data['refresh_token'] = refresh_token
            employee_data['donetasks'] = PlainTaskDoneSchema(many=True).dump(employee.donetasks)
            employee_data['newtasks'] = PlainNewTaskSchema(many=True).dump(employee.newtasks)

            return {
                "message":"Login successfully",
                "data": employee_data
                }
        
        abort(401,message="Invalid credentials.")


@blp.route("/employee/refresh")
class EmployeeTokenRefresh(MethodView):
    @jwt_required(fresh=True)
    def post(self):
        current_employee = get_jwt_identity()
        new_token = create_access_token(identity=current_employee,fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {
            "access_token": new_token
            }        

@blp.route("/employee/register")     
class EmployeeRegister(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200,EmployeeSchema(many=True))
    def get(self):
        return EmployeeModel.query.all()    
    
    @blp.arguments(EmployeeSchema)
    @blp.response(201,EmployeeSchema)
    @jwt_required(fresh=True)
    def post(self,employee_data):

        employee_data["password"] = pbkdf2_sha256.hash(employee_data["password"])
        
        employee = EmployeeModel(**employee_data)

        try:
            db.session.add(employee)
            db.session.commit()

        except IntegrityError:
            abort(400,message="An employee with similar details already exists")    

        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred creating a new employee"
            )     

        return {
            "message":"Employee created successfully",
            "data": employee
            }   
    
@blp.route("/employee/logout")
class EmployeeLogout(MethodView):
    @jwt_required(fresh=True)
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "You successfully logged out"}    
    