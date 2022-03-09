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
from flask_jwt_extended import JWTManager


from src.db import db
from src.ma import ma

def create_app(config_filename:str=None):
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['JWT_SECRET_KEY'] = "My secret"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(user, url_prefix ="/user/")
    app.register_blueprint(cat, url_prefix = "/category/")
    app.register_blueprint(exp, url_prefix = "/expense/")

    db.init_app(app)
    ma.init_app(app)

    jwt = JWTManager(app)


    return app, jwt