import json
from shutil import ExecError
from flask import Blueprint, jsonify, request
from src.models.expense import ExpenseModel

exp = Blueprint(name="expenses", import_name = __name__)

#-------------------------CRUD------------------
@exp.get("/")
def get_expenses():
    expenses = ExpenseModel.find_expenses()
    expenses_list = [expense.json() for expense in expenses]
    return jsonify({"response":expenses_list})

@exp.get("/<int:id>")
def get_expense(id):
    expense = ExpenseModel.find_expense_by_id(id)
    return jsonify({"response":expense.json()})

@exp.post("/create")
def create_expense():
    expense_json = request.json
    expense = ExpenseModel(**expense_json)
    expense.save_to_db()
    return jsonify({"response":"expense has been created"})


@exp.delete("/<int:id>")
def delete_expense(id):
    expense = ExpenseModel.find_expense_by_id(id)
    expense.delete_from_db()
    return jsonify({"response":"expense has been deleted"})