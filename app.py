import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from blocklist import BLOCKLIST
import models

from resources.customer import blp as CustomerBluePrint
from resources.booking import blp as BookingBluePrint
from resources.donetask import blp as DoneTaskBluePrint
from resources.newtask import blp as NewTaskBluePrint
from resources.cashier import blp as CashierBluePrint
from resources.employee import blp as EmployeeBluePrint
from resources.invoice import blp as InvoiceBluePrint
 
def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Xpress REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["JWT_SECRET_KEY"] = "xpress-backend-key"

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {
                    "message": "The token has expired",
                    "error": "token_expired"
                }
            ),
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_loader(error):
        return (
            jsonify(
                {
                    "message":"Signature verification failed",
                    "error": "Invalid_token"
                }
            ),
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token",
                    "error": "authorization_required"
                }
            ),
            401,
        )
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {
                    "description": "The token has been revoked",
                    "error": "token_revoked"
                }
            ),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh",
                    "error": "fresh_token_required"
                }
            )
        )

    db.init_app(app=app)
    api = Api(app=app)

    migrate = Migrate(app=app,db=db)

    api.register_blueprint(CustomerBluePrint)
    api.register_blueprint(BookingBluePrint)
    api.register_blueprint(DoneTaskBluePrint)
    api.register_blueprint(NewTaskBluePrint)
    api.register_blueprint(CashierBluePrint)
    api.register_blueprint(EmployeeBluePrint)  
    api.register_blueprint(InvoiceBluePrint)  
   
    return app