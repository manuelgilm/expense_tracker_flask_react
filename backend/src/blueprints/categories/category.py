import json
from types import BuiltinFunctionType
from unicodedata import category
from flask import Blueprint, jsonify, request
from src.models.category import CategoryModel

cat = Blueprint(name="categoris", import_name = __name__)

# -------------CRUD categories------------------
@cat.get("/")
def get_categories():
    categories = CategoryModel.find_categories()
    categories_list = [category.json() for category in categories]
    return jsonify({"response":categories_list})

@cat.post("/create")
def create_category():
    category_json = request.json
    category = CategoryModel(**category_json)
    category.save_to_db()
    return {"response":"category has been created"}

@cat.get("/<int:id>")
def get_category(id):
    category = CategoryModel.find_category_by_id(id)
    return jsonify({"response":category.json()})

@cat.delete("/<int:id>")
def delete_category(id):
    category = CategoryModel.find_category_by_id(id)
    category.delete_from_db()
    return jsonify({"response":"category has been deleted"})



