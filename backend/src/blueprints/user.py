from gettext import gettext
import json

from src.db import db
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src import responses
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
#---------------USER ENDPOINTS-----------------

user_schema = UserSchema()

@user.get("/")
@jwt_required()
def get_users():
    users = UserModel.find_users()
    users = user_schema.dump(users, many=True)
    return jsonify(users), responses.HTTP_200_OK

@user.post("/create")
# @jwt_required()
def create_user():
    try:
        user = user_schema.load(request.get_json(),session=db.session)
    except ValidationError as err:
        return err.messages, responses.HTTP_400_BAD_REQUEST

    user.save_to_db()
    return jsonify(response = responses.ELEMENT_CREATED.format("User")) , responses.HTTP_201_CREATED

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
    return jsonify(response= responses.DELETED.format("User")) , responses.HTTP_204_NO_CONTENT

@user.post("/login")
def login():
    user_obj = user_schema.load(request.get_json())
    user = UserModel.find_by_username(user_obj.username)
    if user:
        if safe_str_cmp(user.password, user_obj.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return jsonify(access_token = access_token, refresh_token = refresh_token), responses.HTTP_200_OK
    else: 
        return jsonify(response = responses.ELEMENT_NOT_FOUND.format("User")), responses.HTTP_404_NOT_FOUND
    return jsonify(response = responses.INVALID_CREDENTIALS) , responses.HTTP_401_UNAUTHORIZED

@user.post("/logout")
@jwt_required()
def post():
    jti = get_jwt()["jti"]
    user_id = get_jwt_identity()
    BLOCKLIST.add(jti)
    return jsonify(response = responses.LOGOUT), responses.HTTP_200_OK



    




