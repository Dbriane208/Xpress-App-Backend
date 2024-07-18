from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from db import db
from models import DoneTaskModel
from schemas import TaskDoneSchema, TaskDoneUpdateSchema

import logging

logger = logging.getLogger(__name__)

blp = Blueprint("DoneTasks","donetasks",description="Operations on done tasks")

@blp.route("/donetask/<int:donetask_id>")
class DoneTasks(MethodView):
    @blp.response(200,TaskDoneSchema)
    def get(self,donetask_id):
        donetask = DoneTaskModel.query.get_or_404(donetask_id)
        return donetask
    
    def delete(self,donetask_id):
        donetask = DoneTaskModel.query.get_or_404(donetask_id)

        db.session.delete(donetask)
        db.session.commit()

        return {"message":"Task done deleted successfully"}
    
    @blp.arguments(TaskDoneUpdateSchema)
    @blp.response(200,TaskDoneSchema)
    def put(self,donetask_data, donetask_id):

        donetask = DoneTaskModel.query.get_or_404(donetask_id)

        for key, value in donetask_data.items():
            setattr(donetask, key, value)

        db.session.commit()

        return donetask

@blp.route("/donetask")
class DoneTaskList(MethodView):
    @blp.response(200, TaskDoneSchema(many=True))
    def get(self):
        return DoneTaskModel.query.all() 

    @blp.arguments(TaskDoneSchema) 
    @blp.response(201,TaskDoneSchema) 
    def post(self,donetask_data):

        logger.info("Received done task data: %s",donetask_data)

        # existing_task = DoneTaskModel.query.filter_by(carReg=donetask_data['carReg']).first()

        # if existing_task:
        #     abort(400, message="Duplicate")

        donetask = DoneTaskModel(**donetask_data)

        try:
            db.session.add(donetask)
            db.session.commit()
        except IntegrityError as e:
            logger.error("Integrity error while adding completed task: %s",str(e))
            abort(
                400,
                message="A task done with similar details already exists"
            )
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error while adding completed task: %s",str(e))
            abort(
                500,
                message="An error occurred creating a new completed task"
            )
        
        return donetask     