from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import BookingModel
from schemas import BookingSchema, BookingSchemaUpdate

blp = Blueprint("Bookings", "bookings", description="Operations on Bookings")

@blp.route("/booking/<int:booking_id>")
class Booking(MethodView):
    @blp.response(200, BookingSchema)
    def get(self, booking_id):
        booking = BookingModel.query.get_or_404(booking_id)
        return booking
    
    def delete(self, booking_id):
        booking = BookingModel.query.get_or_404(booking_id)
        db.session.delete(booking)
        db.session.commit()
        return {"message": "Booking deleted successfully"}
    
    @blp.arguments(BookingSchemaUpdate)
    @blp.response(200, BookingSchema)
    def put(self, booking_data, booking_id):
        booking = BookingModel.query.get_or_404(booking_id)

        for key, value in booking_data.items():
            setattr(booking, key, value)

        db.session.commit()
        return booking

@blp.route("/booking")
class BookingList(MethodView):
    @blp.response(200, BookingSchema(many=True))
    def get(self):
        return BookingModel.query.all()
    
    @blp.arguments(BookingSchema)
    @blp.response(201, BookingSchema)
    def post(self, booking_data):
        booking = BookingModel(**booking_data)

        try:
            db.session.add(booking)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A booking with similar details already exists"
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred creating a new booking"
            )
        
        return booking
