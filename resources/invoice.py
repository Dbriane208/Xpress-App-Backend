from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import InvoiceModel
from schemas import InvoiceSchema, InvoiceUpdateSchema

blp  = Blueprint("Invoices","invoices","Operation on invoices")

@blp.route("/invoice/<int:invoice_id>")
class Invoice(MethodView):
    @blp.response(200,InvoiceSchema)
    def get(self,invoice_id):
        invoice = InvoiceModel.query.get_or_404(invoice_id)
        return invoice
    
    def delete(self,invoice_id):
        invoice = InvoiceModel.query.get_or_404(invoice_id)
        
        db.session.delete(invoice)
        db.session.all()

        return invoice
    
    @blp.arguments(InvoiceUpdateSchema)
    @blp.response(201,InvoiceSchema)
    def put(self,invoice_data,invoice_id):
        
        invoice = InvoiceModel.query.get_or_404(invoice_id)

        for key, value in invoice_data.items():
            setattr(invoice, key, value)

        db.session.commit()

        return invoice


@blp.route("/invoice")
class InvoiceList(MethodView):
    @blp.response(200,InvoiceSchema(many=True))
    def get(self):
        return InvoiceModel.query.all()

    @blp.arguments(InvoiceSchema)
    @blp.response(201,InvoiceSchema)
    def post(self,invoice_data):

        invoice = InvoiceModel(**invoice_data)

        try:
            db.session.add(invoice)
            db.session.commit()

        except IntegrityError:
            abort(
                400,
                message="An Invoice with similar details already exists"
            )    

        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred creating a new invoice"
            )  

        return invoice          