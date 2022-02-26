import json
from types import BuiltinFunctionType
from unicodedata import category
from flask import Blueprint, jsonify, request
from src.models.category import CategoryModel
from src.schemas.category import CategorySchema

cat = Blueprint(name="categoris", import_name = __name__)

cat_schema = CategorySchema()

# -------------CRUD categories------------------
@cat.get("/")
def get_categories():
    categories = CategoryModel.find_categories()
    return jsonify(cat_schema.dump(categories, many = True))

@cat.post("/create")
def create_category():
    category = cat_schema.load(request.get_json())
    category.save_to_db()
    return {"response":"category has been created"}

@cat.get("/<int:id>")
def get_category(id):
    category = CategoryModel.find_category_by_id(id)
    return jsonify({"response":cat_schema.dump(category)})

@cat.delete("/<int:id>")
def delete_category(id):
    category = CategoryModel.find_category_by_id(id)
    category.delete_from_db()
    return jsonify({"response":"category has been deleted"})



