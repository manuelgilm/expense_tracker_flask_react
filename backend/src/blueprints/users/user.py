import json
from flask import Blueprint, request, jsonify
from src.models.user import UserModel
user = Blueprint(name="users", import_name=__name__)


#---------------USER CRUD-----------------
@user.get("/")
def get_users():
    users = UserModel.find_users()
    users_dict = [user.json() for user in users]
    print(users_dict)
    return jsonify({"response":users_dict})

@user.post("/create")
def create_user():
    user_json = request.json
    print(user_json)
    user = UserModel(username=user_json["username"], password=user_json["password"])
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

    




