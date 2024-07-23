from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from db import db
from models import CustomerModel
from schemas import CustomerSchema, CustomerUpdateSchema, CustomerLoginSchema
from schemas.booking_schema import PlainBookingSchema
from schemas.invoice_schema import PlainInvoiceSchema

blp = Blueprint("Customers", "customers", description="Operations on customers")

@blp.route("/customer/<int:customer_id>")
class Customer(MethodView):
    @blp.response(200, CustomerSchema)
    def get(self, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        return customer
    
    def delete(self, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)

        db.session.delete(customer)
        db.session.commit()

        return {"message": "Customer deleted successfully"}
    
    @blp.arguments(CustomerUpdateSchema)
    @blp.response(200, CustomerSchema)
    def put(self, customer_data, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)

        for key, value in customer_data.items():
            setattr(customer, key, value)

        db.session.commit()

        return customer 
    
@blp.route("/customer/login")
class CustomerLogin(MethodView):
    @blp.arguments(CustomerLoginSchema) 
    def post(self, customer_data):
        customer = CustomerModel.query.filter(
            CustomerModel.email == customer_data["email"]
        ).first()  

        if customer and pbkdf2_sha256.verify(customer_data["password"], customer.password):
            access_token = create_access_token(identity=customer.id)
            customer_data = CustomerSchema().dump(customer)
            customer_data['access_token'] = access_token
            customer_data['bookings'] = PlainBookingSchema(many=True).dump(customer.bookings)
            customer_data['invoices'] = PlainInvoiceSchema(many=True).dump(customer.invoices)

            return {
               "message": "Login successfully",
               "data": customer_data
                }

        abort(409, message="Invalid Credentials") 

@blp.route("/customer/register")
class CustomerRegister(MethodView):
    @blp.response(200, CustomerSchema(many=True))
    def get(self):
        return CustomerModel.query.all()
    
    @blp.arguments(CustomerSchema)
    @blp.response(201, CustomerSchema)
    def post(self, customer_data):
      customer_data["password"] = pbkdf2_sha256.hash(customer_data["password"])

      customer = CustomerModel(**customer_data)

      try:
        db.session.add(customer)
        db.session.commit()

      except IntegrityError:
        abort(400, message="A customer with similar details already exists")

      except SQLAlchemyError:
        abort(500, message="An error occurred creating a new customer")

      return {
         "message":"Registration successful",
         "data": customer
        }
 


