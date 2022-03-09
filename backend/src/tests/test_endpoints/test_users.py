from cgi import test
from src.app import create_app 
import json


def test_user_init_page(test_client):
    '''
    GIVEN a Flask application configured for testing 
    WHEN the '/user/init' page is get
    THEN check that a '200' status code and the string "OK" are returned.
    '''

    response = test_client.get("/user/init")
    assert response.status_code == 200
    assert response.json["response"] == "OK"

def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/user/login', 
                                data = json.dumps({"username":"manuelito", "password":"password1"}),
                                content_type='application/json')
    print("T"*100)
    print(response)
    assert response.status_code == 200

