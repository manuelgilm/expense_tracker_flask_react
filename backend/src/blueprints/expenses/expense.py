import json
from src.db import db
from shutil import ExecError
from flask import Blueprint, jsonify, request
from src.models.expense import ExpenseModel
from src.schemas.expense import ExpenseSchema
from src.models.category import CategoryModel

exp = Blueprint(name="expenses", import_name = __name__)

expense_schema = ExpenseSchema()
#-------------------------CRUD------------------
@exp.get("/")
def get_expenses():
    expenses = ExpenseModel.find_expenses()
    expenses = expense_schema.dump(expenses, many = True)
    return jsonify(expenses)

@exp.get("/<int:id>")
def get_expense(id):
    expense = ExpenseModel.find_expense_by_id(id)
    return jsonify({"response":expense_schema.dump(expense)})

@exp.post("/create")
def create_expense():
    expense = expense_schema.load(request.get_json())
    expense.save_to_db()
    return jsonify({"response":"expense has been created"})


@exp.delete("/<int:id>")
def delete_expense(id):
    expense = ExpenseModel.find_expense_by_id(id)
    expense.delete_from_db()
    return jsonify({"response":"expense has been deleted"})