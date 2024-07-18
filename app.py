import os
from flask import Flask
from flask_smorest import Api

from db import db
import models

from resources.customer import blp as CustomerBluePrint
from resources.booking import blp as BookingBluePrint
from resources.donetask import blp as DoneTaskBluePrint
from resources.newtask import blp as NewTaskBluePrint
# from resources.cashier import blp as CashierBluePrint
from resources.employee import blp as EmployeeBluePrint
# from resources.invoice import blp as InvoiceBluePrint
 



def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Xpress REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")

    db.init_app(app=app)
    api = Api(app=app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(CustomerBluePrint)
    api.register_blueprint(BookingBluePrint)
    api.register_blueprint(DoneTaskBluePrint)
    api.register_blueprint(NewTaskBluePrint)
    # api.register_blueprint(CashierBluePrint)
    api.register_blueprint(EmployeeBluePrint)  
    # api.register_blueprint(InvoiceBluePrint)  
   
    return app