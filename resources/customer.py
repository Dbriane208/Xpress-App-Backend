from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from db import db
from models import CustomerModel
from schemas import CustomerSchema,CustomerUpdateSchema

blp = Blueprint("Customers","customers",description="Operations on customers")

@blp.route("/customer/<int:customer_id>")
class Customer(MethodView):
    @blp.response(200,CustomerSchema)
    def get(self,customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        return customer
    
    def delete(self,customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)

        db.session.delete(customer)
        db.session.commit()

        return {"message":"Customer deleted successfully"}
    
    @blp.arguments(CustomerUpdateSchema)
    @blp.response(200,CustomerSchema)
    def put(self, customer_data, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)

        for key, value in customer_data.items():
            setattr(customer, key, value)

        db.session.commit()

        return customer 

    
@blp.route("/customer")
class CustomerList(MethodView):
    @blp.response(200,CustomerSchema(many=True))    
    def get(self):
        return CustomerModel.query.all()
    
    @blp.arguments(CustomerSchema)
    @blp.response(201,CustomerSchema)
    def post(self,customer_data):

        customer = CustomerModel(**customer_data)

        try:
            db.session.add(customer)
            db.session.commit()
        
        except IntegrityError:
            abort(
                400,
                message="A customer with similar details already exists"
            )

        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred creating a new customer"
            )  

        return customer      
        