from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CashierModel
from schemas import CashierSchema, CashierUpdateSchema

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
    

@blp.route("/cashier")
class CashierList(MethodView):
    @blp.response(200,CashierSchema(many=True))
    def get(self):
        return CashierModel.query.all()

    @blp.arguments(CashierSchema)
    @blp.response(201,CashierSchema)
    def post(self,cashier_data):

        cashier = CashierModel(**cashier_data)

        try:
            db.session.add(cashier)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A cashier with similar details already exists"
            
            )      

        except SQLAlchemyError:
            abort(
               500,
               message="An error occurred creating a new cashier" 
            )   

        return cashier    