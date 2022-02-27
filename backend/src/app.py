from flask import Flask
from flask_cors import CORS

#load models
from src.models.category import CategoryModel
from src.models.user import UserModel
from src.models.expense import ExpenseModel

#load modules
from src.blueprints.user import user
from src.blueprints.category import cat
from src.blueprints.expense import exp


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JWT_SECRET_KEY'] = "My secret"

app.register_blueprint(user, url_prefix ="/user/")
app.register_blueprint(cat, url_prefix = "/category/")
app.register_blueprint(exp, url_prefix = "/expense/")