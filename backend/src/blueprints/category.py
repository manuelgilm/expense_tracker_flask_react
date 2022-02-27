from src.db import db
from unicodedata import category
from flask import Blueprint, jsonify, request
from src.models.category import CategoryModel
from src.schemas.category import CategorySchema
from flask_jwt_extended import jwt_required, get_jwt_identity
cat = Blueprint(name="categoris", import_name = __name__)

cat_schema = CategorySchema()

# -------------CRUD categories------------------
@cat.get("/")
@jwt_required()
def get_categories():
    current_user_id = get_jwt_identity()
    categories = CategoryModel.find_categories_by_owner(current_user_id)
    return jsonify(cat_schema.dump(categories, many = True))

@cat.post("/create")
@jwt_required()
def create_category():
    data = request.get_json()
    data.update({"user_id":get_jwt_identity()})
    category = cat_schema.load(data, session=db.session)
    category.save_to_db()
    return {"response":"category has been created"}

@cat.get("/<int:id>")
@jwt_required()
def get_category(id):
    category = CategoryModel.find_category_by_id(id)
    return jsonify({"response":cat_schema.dump(category)})

@cat.delete("/<int:id>")
@jwt_required()
def delete_category(id):
    category = CategoryModel.find_category_by_id(id)
    category.delete_from_db()
    return jsonify({"response":"category has been deleted"})



