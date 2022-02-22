import json
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.models.user import UserModel
from src.schemas.user import UserSchema
from src.ma import ma

user = Blueprint(name="users", import_name=__name__)


#---------------USER CRUD-----------------

user_schema = UserSchema()

@user.get("/")
def get_users():
    users = UserModel.find_users()
    users_dict = [user.json() for user in users]
    print(users_dict)
    return jsonify({"response":users_dict})

@user.post("/create")
def create_user():
    try:
        user = user_schema.load(request.json)
    except ValidationError as err:
        return err.messages, 400
    user.save_to_db()
    return jsonify({"response":"user created"})

@user.get("/<int:id>")
def get_user_by_id(id):
    user = UserModel.find_by_id(id)
    return jsonify({"response":user.json()})

@user.delete("/<int:id>")
def delete_user(id):
    user = UserModel.find_by_id(id)
    user.delete_from_db()
    return jsonify({"response":"user has been deleted"})

    




