from gettext import gettext

from src.db import db
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.models.user import UserModel
from src.schemas.user import UserSchema
from src.ma import ma
from src.blocklist import BLOCKLIST
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

user = Blueprint(name="users", import_name=__name__)

#---------------USER CRUD-----------------

user_schema = UserSchema()

@user.get("/")
@jwt_required()
def get_users():
    users = UserModel.find_users()
    users = user_schema.dump(users, many=True)
    
    
    # users_dict = [user.json() for user in users]
    # print(users_dict)
    # return jsonify({"response":users_dict})
    return jsonify(users)

@user.post("/create")
@jwt_required()
def create_user():
    try:
        user = user_schema.load(request.get_json(),session=db.session)
    except ValidationError as err:
        return err.messages, 400
    user.save_to_db()
    return jsonify({"response":"user created"})

@user.get("/<int:id>")
@jwt_required()
def get_user_by_id(id):
    user = UserModel.find_by_id(id)
    return user.dump()

@user.delete("/<int:id>")
@jwt_required()
def delete_user(id):
    user = UserModel.find_by_id(id)
    user.delete_from_db()
    return jsonify({"response":"user has been deleted"})

@user.post("/login")
def login():
    user_json = request.get_json()
    user_obj = user_schema.load(user_json)

    user = UserModel.find_by_username(user_obj.username)

    if user and safe_str_cmp(user.password, user_obj.password):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200

    return {"response":"Invalid credentials"}, 401

@user.post("/logout")
@jwt_required()
def post():
    jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
    user_id = get_jwt_identity()
    BLOCKLIST.add(jti)
    return {"message": "user_logged_out"}, 200



    




