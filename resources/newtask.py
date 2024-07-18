from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import NewTaskModel
from schemas import NewTaskSchema, NewTaskUpdateSchema

import logging

logger = logging.getLogger(__name__)

blp = Blueprint("NewTasks","newtasks","Operations on new tasks")

@blp.route("/newtask/<int:newtask_id>")
class NewTasks(MethodView):
    @blp.response(200,NewTaskSchema)
    def get(self,newtask_id):
        newtask = NewTaskModel.query.get_or_404(newtask_id)
        return newtask
    
    def delete(self,newtask_id):
        newtask = NewTaskModel.query.get_or_404(newtask_id)

        db.session.delete(newtask)
        db.session.commit()

        return {"message":"New Task deleted successfully"}
    
    @blp.arguments(NewTaskUpdateSchema)
    @blp.response(200,NewTaskSchema)
    def put(self,newtask_data, newtask_id):
        newtask = NewTaskModel.query.get_or_404(newtask_id)

        for key, value in newtask_data.items():
            setattr(newtask, key, value)

        db.session.commit()

        return newtask


@blp.route("/newtask")
class NewTaskList(MethodView):
    @blp.response(200,NewTaskSchema())
    def get(self):
        return NewTaskModel.query.all()

    @blp.arguments(NewTaskSchema) 
    @blp.response(201,NewTaskSchema) 
    def post(self,newtask_data):

        logger.info("Received newtask data: %s", newtask_data)

        newtask = NewTaskModel(**newtask_data)

        try:
            db.session.add(newtask)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A task with similar details already exists"
            )
            
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error while adding new task %s", str(e))
            abort(
                500,
                message="An error occurred creating a new assigned task"
            )
        
        return newtask    
