import json 
from src.models.category import CategoryModel
from flask_jwt_extended import create_access_token, get_jwt_identity

def test_create_category(test_client,init_database):
    '''
    GIVEN a Flask application configured for testing.
    WHEN the '/category/create' endpoint receives a request.
    THEN check that a 201 status code and the string "{category_name} created!" are returned.
    '''
    #login default user
    response = test_client.post('/user/login', 
                                data = json.dumps({"username":"manuelito", "password":"password1"}),
                                content_type='application/json')

    assert response.status_code == 200

    #Create the category
    access_token = response.json["access_token"]
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.post('/category/create',
                                data = json.dumps({'name':'new category', 'description':'category description'}),
                                headers = headers,
                                content_type = 'application/json')
    assert response.status_code == 201
    assert response.json['response'] == 'new category created!'