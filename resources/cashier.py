from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from db import db
from models import CashierModel
from schemas import CashierSchema, CashierUpdateSchema, CashierLoginSchema, PlainNewTaskSchema

blp = Blueprint("Cashiers","cashiers","Operations on cashiers")


@blp.route("/cashier/<int:cashier_id>")
class Cashier(MethodView):
    @blp.response(200,CashierSchema)
    def get(self,cashier_id):
        cashier = CashierModel.query.get_or_404(cashier_id)
        return cashier
    
    def delete(self,cashier_id):
        cashier = CashierModel.query.get_or_404(cashier_id)

        db.session.delete(cashier)
        db.session.commit()

        return {"message":"Cashier deleted successfully"}
    
    @blp.arguments(CashierUpdateSchema)
    @blp.response(200,CashierSchema)
    def put(self,cashier_data, cashier_id):
        cashier = CashierModel.query.get_or_404(cashier_id)

        for key, value in cashier_data.items():
            setattr(cashier, key, value)

        db.session.commit()

        return cashier
    
    
@blp.route("/cashier/login")
class  CashierLogin(MethodView):
    @blp.arguments(CashierLoginSchema)
    def post(self,cashier_data):

        cashier = CashierModel.query.filter(
            CashierModel.email == cashier_data["email"]
        ).first()

        if cashier and pbkdf2_sha256.verify(cashier_data["password"],cashier.password):
            access_token = create_access_token(identity=cashier.id)
            cashier_data = CashierSchema().dump(cashier)
            cashier_data['access_token'] = access_token
            cashier_data['newtasks'] = PlainNewTaskSchema(many=True).dump(cashier.newtasks)

            return {
                "message":"Login successfully",
                "data": cashier_data
                }
        
        abort(401,message="Invalid Credentials")


@blp.route("/cashier/register")
class CashierRegister(MethodView):
    @blp.response(200,CashierSchema(many=True))
    def get(self):
        return CashierModel.query.all()

    @blp.arguments(CashierSchema)
    @blp.response(201,CashierSchema)
    def post(self,cashier_data):

        if CashierModel.query.filter(CashierModel.email == cashier_data["email"]).first():
            abort(409,message="A cashier with similar details already exists")

        cashier_data['password'] = pbkdf2_sha256.hash(cashier_data['password'])    

        cashier = CashierModel(**cashier_data)

        try:
            db.session.add(cashier)
            db.session.commit()    

        except SQLAlchemyError:
            abort(
               500,
               message="An error occurred creating a new cashier" 
            )   

        return {
            "message":"cashier created successfully",
            "data": cashier
            } 