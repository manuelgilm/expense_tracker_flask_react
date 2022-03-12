'''
Each one of the following tests should be made by a registered user, for that reason, 
before starting the test with the target endpoint, first, a login request should be 
performed.
'''

import json 
from src.models.category import CategoryModel
from flask_jwt_extended import create_access_token, get_jwt_identity

def test_create_category(test_client,init_database):
    '''
    GIVEN a Flask application configured for testing.
    WHEN the '/category/create' endpoint receives a request.
    THEN check 
        - that a 201 status code is returned indicating the category has been created.
        - that the string "{category_name} created!" is returned.
    '''
    #login default user
    response = test_client.post('/user/login', 
                                data = json.dumps({"username":"user1", "password":"password2"}),
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

def test_get_category_by_id(test_client, init_database):
    '''
    GIVEN a Flask application configured for testing.
    WHEN the '/category/<category_id:int>' endpoint receives a request.
    THEN check 
        - that a 200 status code is returned indicating everything went ok.
        - that the category name "is Category 1"
        - that the category description is "Category 1 description"
        - that the data type of expenses within the category is a list
    '''
    #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = test_client.get('/category/1',
                                headers = headers,
                                content_type = 'application/json')

    assert response.status_code == 200
    assert response.json['response']['name'] == 'Category 1'
    assert response.json['response']['description'] == 'Category 1 description'
    assert type(response.json['response']['expenses']) == list
    assert len(response.json['response']['expenses']) == 2

def test_get_list_categories_by_owner(test_client, init_database):
    '''
    GIVEN a Flask application configured for testing.
    WHEN the /category/list endpoint receives a request
    THEN check
        - that the status code returned is 200 indicating everything went OK
        - that the categories returned are the categories that belong to the user
        - that the data type of the response corresponds to list
    '''

   #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    #categories request
    response = test_client.get('/category/list',
                                headers = headers,
                                content_type = 'application/json')

    user_categories = CategoryModel.find_categories_by_owner(1)
    user_categories = [cat.name for cat in user_categories]
    categories_in_request = [cat['name'] for cat in response.json['response']]

    assert response.status_code == 200
    assert user_categories == categories_in_request
    assert type(response.json['response']) == list

def test_delete_category(test_client, init_database):
    '''
    GIVEN a Flask application configured for testing.
    WHEN the /category/<int:id> endpoint receives a request.
    THEN check
        - The status code returned is 204 indicating the item has been deleted
    '''
    #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    #categories request
    response = test_client.delete('/category/1',
                                headers = headers,
                                content_type = 'application/json')
    assert response.status_code == 204