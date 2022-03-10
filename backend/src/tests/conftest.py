import json
import pytest
from src.app import create_app
from src.db import db
from src.models.user import UserModel
from src.schemas.user import UserSchema
from werkzeug.security import generate_password_hash


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


@pytest.fixture(scope="module")
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = UserModel(username = "manuelito", password = generate_password_hash("password1"))
    user2 = UserModel(username = "manuelito2", password = generate_password_hash("password2"))
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope="session")
def login_default_user(test_client):
    test_client.post("/user/login",
                     data = json.dumps(dict(username="manuelito", password=generate_password_hash("password1"))),
                     content_type='application/json')


    yield  # this is where the testing happens!

    test_client.get("/user/logout", follow_redirects=True)
