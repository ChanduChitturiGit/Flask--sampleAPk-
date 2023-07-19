from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
import uuid
from schemas import StoreSchema
import models
from models.store_model import StoreModel
from models.items_model import ItemsModel
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required,get_jwt


blp = Blueprint("Stores",__name__,description="Stores Module.")


@blp.route('/stores/getAllStores')
class GetAll(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    
@blp.route("/stores/getStorebyId/<int:id>")
class GetStorebyId(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema)
    def get(self,id):
        data = StoreModel.query.get_or_404(id)
        if data:
            return data
        else:
            abort(400,message="Store not found.")


@blp.route('/stores/addStore')
class AddStore(MethodView):
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="Authentication Failed.")
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store already Exisits.")
        except SQLAlchemyError:
            abort(500,message="Unexpected error during creation of store.")  
        return new_store
        

@blp.route('/stores/deleteStore/<int:id>')
class DeleteStore(MethodView):
    @jwt_required()
    @blp.response(200)
    def delete(self,id):
        store_data = StoreModel.query.get_or_404(id)
        items_data = ItemsModel.query.get_or_404(store_id=id)
        if store_data:
            if items_data:
                db.session.delete(items_data)
                db.session.commit()
            db.session.delete(store_data)
            db.session.commit()
            return "Store deleted."
        else:
            abort(400,message="Store not Found")