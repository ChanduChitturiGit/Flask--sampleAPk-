from flask import request,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
import uuid
from schemas import StoreSchema,UserSchema
import models
from models.store_model import StoreModel
from models.items_model import ItemsModel
from models.user_model import UserModel
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,jwt_required,get_jwt
import jwt
from datetime import *
from .blockList import blockList



blp = Blueprint("users",__name__,description="User Module.")


@blp.route("/users/register")
class Register(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self,user_data):
        data = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if data:
            abort(409,message="User already exisits.")
        new_user = UserModel(
                username = user_data["username"],
                password = pbkdf2_sha256.hash(user_data["password"]),
                role = "user"    
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user


@blp.route("/users/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        data = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if data and pbkdf2_sha256.verify(user_data["password"], data.password):
            access_token = create_access_token(identity={"id":data.id,"role":data.role})
            # token = jwt.encode(
            #     {``
            #         "id":data.id,
            #         'expiration': str(datetime.utcnow() + timedelta(seconds=200))
            #     },
            # 'SECRET_KEY')
            # return token
            
            return {"access_token":access_token},200
        abort(400,message="User not Found.")  
        
        
@blp.route('/users/logout')
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        blockList.add(jti)
        return "Logout Successfull.",200