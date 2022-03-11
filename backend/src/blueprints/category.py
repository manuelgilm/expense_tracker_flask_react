from gc import get_objects
from http.client import responses
import json
from src.db import db
from unicodedata import category
from flask import Blueprint, jsonify, request
from src import responses
from src.models.category import CategoryModel
from src.schemas.category import CategorySchema
from flask_jwt_extended import jwt_required, get_jwt_identity
cat = Blueprint(name="categoris", import_name = __name__)

cat_schema = CategorySchema()

# -------------CRUD categories------------------
@cat.get("/list")
@jwt_required()
def get_categories():
    current_user_id = get_jwt_identity()
    categories = CategoryModel.find_categories_by_owner(current_user_id)
    return jsonify(response = cat_schema.dump(categories, many = True)), responses.HTTP_200_OK

@cat.post("/create")
@jwt_required()
def create_category():
    data = request.get_json()
    data.update({"user_id":get_jwt_identity()})
    print(data)
    category = cat_schema.load(data, session=db.session)
    category_prev = CategoryModel.find_category_by_name_and_owner(category_name=category.name, user_id=get_jwt_identity())
    if category_prev:
        return jsonify(response = responses.ELEMENT_ALREADY_EXISTS.format(category.name)), responses.HTTP_400_BAD_REQUEST

    category.save_to_db()
    return jsonify(response = responses.ELEMENT_CREATED.format(category.name)), responses.HTTP_201_CREATED

@cat.get("/category/<string:category_name>")
@jwt_required
def get_category_by_name(category_name):
    category = CategoryModel.find_category_by_name_and_owner(category_name=category_name, user_id=get_jwt_identity())
    if category:
        return jsonify(response= cat_schema.dump(category)), responses.HTTP_200_OK
    return jsonify(response = responses.ELEMENT_NOT_FOUND.format(category_name)), responses.HTTP_400_BAD_REQUEST

@cat.get("/<int:id>")
@jwt_required()
def get_category(id):
    category = CategoryModel.find_category_by_id(id)
    if category:
        return jsonify(response = cat_schema.dump(category)), responses.HTTP_200_OK
    return jsonify(response = responses.ELEMENT_NOT_FOUND.format("Category")), responses.HTTP_400_BAD_REQUEST

@cat.delete("/<int:id>")
@jwt_required()
def delete_category(id):
    category = CategoryModel.find_category_by_id(id)
    if category:
        category.delete_from_db()
        return jsonify(response = responses.DELETED.format("Category")), responses.HTTP_204_NO_CONTENT
    return jsonify(response = responses.ELEMENT_NOT_FOUND.format("Category")), responses.HTTP_400_BAD_REQUEST

#add endpoint to update categories



