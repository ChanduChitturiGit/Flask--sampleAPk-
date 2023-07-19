from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
import uuid
from schemas import ItemsSchema,ItemsUpdateSchema
from models.store_model import StoreModel
from models.items_model import ItemsModel
from flask_smorest import abort
from flask_jwt_extended import jwt_required


blp = Blueprint("Items",__name__,description="Items Module.")

@blp.route("/items/<int:id>")
class ItemsbyId(MethodView):
    @jwt_required()
    @blp.response(200,ItemsSchema)
    def get(self,id):
        data=ItemsModel.query.get(id)
        if data:
            return data
        abort(400,message="Data not found.")
        
        
@blp.route("/items/getitems/<int:store_id>")
class ItemsbyStoreId(MethodView):
    @jwt_required()
    @blp.response(200,ItemsSchema(many=True))
    def get(self,store_id):
        data=StoreModel.query.get(store_id)
        if data and data.items.all():
            return data.items.all()
        abort(400,message="Data not found.")

    
@blp.route("/items/add")
class AddItems(MethodView):
    @jwt_required()    
    @blp.arguments(ItemsSchema)
    @blp.response(201,ItemsSchema)
    def post(self,request_data):
        # request_data = request.get_json()
        data=StoreModel.query.get(request_data["store_id"])
        if data:
            new_item = ItemsModel(**request_data)
            db.session.add(new_item)
            db.session.commit()
            return new_item
    
        abort(400,message="Store not found.")
        
    
@blp.route("/items/getAll")
class GetAllItems(MethodView):
    @jwt_required()
    @blp.response(200,ItemsSchema(many=True))
    def get(self):
        return ItemsModel.query.all()