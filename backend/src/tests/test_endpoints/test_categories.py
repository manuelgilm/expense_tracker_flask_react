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
    ----------------------------------------------------------------------------------------
    THEN check that a 200 status code and the string "{category_name} created!" are returned.
    ----------------------------------------------------------------------------------------
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
    DOC
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
    DOC
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