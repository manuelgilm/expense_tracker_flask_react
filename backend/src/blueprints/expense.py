from http.client import ResponseNotReady
import json

from click import get_current_context
from src.db import db
from flask import Blueprint, jsonify, request
from src import responses
from src.models.expense import ExpenseModel
from src.schemas.expense import ExpenseSchema
from src.models.category import CategoryModel
from src.models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity

exp = Blueprint(name="expenses", import_name = __name__)

expense_schema = ExpenseSchema()
#-------------------------CRUD------------------
@exp.get("/")
@jwt_required()
def get_expenses():
    expenses = ExpenseModel.find_expenses_by_owner(get_jwt_identity())
    return jsonify(expense_schema.dump(expenses, many = True)), responses.HTTP_200_OK

@exp.get("/<int:id>")
@jwt_required()
def get_expense(id):
    expense = ExpenseModel.find_expense_by_id_and_owner(expense_id=id, user_id=get_jwt_identity())
    if expense:
        return jsonify(expense_schema.dump(expense)), responses.HTTP_200_OK
    return jsonify(response = responses.ELEMENT_NOT_FOUND.format("Expense")), responses.HTTP_404_NOT_FOUND

@exp.post("/create")
@jwt_required()
def create_expense():
    data = request.get_json()
    category_name = data.pop("category_name", None)
    current_user_id = get_jwt_identity()
    category = CategoryModel.find_category_by_name_and_owner(category_name=category_name, user_id=current_user_id)

    if category:
        data.update({"user_id":current_user_id,"category_id":category.id})
        expense = expense_schema.load(data)
        expense.save_to_db()
        return jsonify(response = responses.ELEMENT_CREATED.format("Expense")), responses.HTTP_201_CREATED
    return jsonify(response = responses.ELEMENT_NOT_FOUND.format("Category")), responses.HTTP_400_BAD_REQUEST


@exp.delete("/<int:id>")
@jwt_required()
def delete_expense(id):
    expense = ExpenseModel.find_expense_by_id(id)
    expenses = ExpenseModel.find_expenses_by_owner(user_id=get_jwt_identity())
    if expense in expenses:
        expense.delete_from_db()
        return jsonify(response = responses.DELETED.format("Expense")), responses.HTTP_204_NO_CONTENT
    return jsonify(response = responses.ELEMENT_NOT_FOUND.format("Expense")), responses.HTTP_404_NOT_FOUND

@exp.get("/total")
@jwt_required()
def total():
    expenses = ExpenseModel.total_expenses_by_user_id(user_id=get_jwt_identity())
    return jsonify(response = expenses[0]), responses.HTTP_200_OK

@exp.get("/total/<int:category_id>")
@jwt_required()
def total_by_category(category_id):
    expenses_category = ExpenseModel.total_expenses_by_category(user_id=get_jwt_identity(), category_id=category_id)
    return jsonify(response = expenses_category[0])
