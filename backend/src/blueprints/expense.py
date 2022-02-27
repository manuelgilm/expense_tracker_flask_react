import json
from src.db import db
from flask import Blueprint, jsonify, request
from src.models.expense import ExpenseModel
from src.schemas.expense import ExpenseSchema
from src.models.category import CategoryModel
from flask_jwt_extended import jwt_required, get_jwt_identity

exp = Blueprint(name="expenses", import_name = __name__)

expense_schema = ExpenseSchema()
#-------------------------CRUD------------------
@exp.get("/")
@jwt_required()
def get_expenses():
    current_user_id = get_jwt_identity()
    expenses = ExpenseModel.find_expenses_by_owner(current_user_id)
    expenses = expense_schema.dump(expenses, many = True)
    return jsonify(expenses)

@exp.get("/<int:id>")
@jwt_required()
def get_expense(id):
    expense = ExpenseModel.find_expense_by_id(id)
    return jsonify({"response":expense_schema.dump(expense)})

@exp.post("/create")
@jwt_required()
def create_expense():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user_categories = CategoryModel.find_categories_by_owner(current_user_id)

    if data["name"] in [category.name for category in user_categories]:
        data.update({"user_id":get_jwt_identity()})
        expense = expense_schema.load(data)
        expense.save_to_db()
        return jsonify({"response":"expense has been created"})

    return jsonify({"response":"Category not Found"}), 404


@exp.delete("/<int:id>")
@jwt_required()
def delete_expense(id):
    expense = ExpenseModel.find_expense_by_id(id)
    expense.delete_from_db()
    return jsonify({"response":"expense has been deleted"})