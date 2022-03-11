import json
import pytest
from src.app import create_app
from src.db import db
from src.models.user import UserModel
from src.models.expense import ExpenseModel
from src.models.category import CategoryModel
from src.schemas.user import UserSchema
from werkzeug.security import generate_password_hash
import random

user_schema = UserSchema


@pytest.fixture(scope="module")
def new_user():
    user = UserModel(username = "Username", password = "password")
    return user

@pytest.fixture(scope="module")
def test_client():
    flask_app , _ = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # users
    user1 = UserModel(username = 'user', password = generate_password_hash('password1'))
    user2 = UserModel(username = 'user1', password = generate_password_hash('password2'))

    #categories
    categories = []
    for n in range(6):
        if n<=3:
            user_id = 1
        else:
            user_id = 2
        print(user_id)
        categories.append(CategoryModel(name = f'Category {n+1}', description= f'Category {n+1} description', user_id = user_id))

    #expenses
    expenses = []
    for n in range(10):
        if n<=3:
            user_id = 1
        else:
            user_id = 2

        expenses.append(ExpenseModel(
            name = f"Expense {n+1}",
            description = f"Expense {n+1} description",
            amount = (n+1.0)*random.randint(500,2000),
            user_id = user_id,
            category_id = n+1 if n <= 6 else n-6
        ))

    db.session.add(user1)
    db.session.add(user2)
    db.session.add_all(categories)
    db.session.add_all(expenses)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

@pytest.fixture(scope="function")
def login_default_user(test_client):
    test_client.post("/user/login",
                     data = json.dumps(dict(username="user", password=generate_password_hash("password1"))),
                     content_type='application/json')
    yield  # this is where the testing happens!
    test_client.get("/user/logout", follow_redirects=True)
