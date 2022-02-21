from flask import Flask
from flask_cors import CORS

#load modules
from src.blueprints.test.test import test
from src.blueprints.users.user import user
from src.blueprints.categories.category import cat
from src.blueprints.expenses.expense import exp

#load models
from src.models.category import CategoryModel
from src.models.user import UserModel
from src.models.expense import ExpenseModel

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.register_blueprint(test, url_prefix = "/test")
app.register_blueprint(user, url_prefix ="/user/")
app.register_blueprint(cat, url_prefix = "/category/")
app.register_blueprint(exp, url_prefix = "/expense/")