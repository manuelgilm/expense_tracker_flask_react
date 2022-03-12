'''
Each one of the following tests should be made by a registered user, for that reason, 
before starting the test with the target endpoint, first, a login request should be 
performed.
'''
import json
from src.models.expense import ExpenseModel

def test_create_expense(test_client, init_database):
    '''
    DESCRIPTION: The endpoint to be tested should create a new expense.

    TEST:
    ----
    GIVEN a Flask application configured for testing.
    WHEN the /expense/create endpoint receives a request.
    THEN check
        - that the status code 201 is returned indicating the expense has been created.
        - that the response object returned the string "Expense created!"
    '''
    #login user
    response = test_client.post('/user/login', 
                                data = json.dumps({"username":"user", "password":"password1"}),
                                content_type='application/json')

    assert response.status_code == 200
    #Create expense
    access_token = response.json["access_token"]
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.post('/expense/create',
                                data = json.dumps({
                                    'name':'new expense',
                                    'description':'new expense description',
                                    'amount':1.0,
                                    'category_name': 'Category 1'
                                    }),
                                headers = headers,
                                content_type = 'application/json')
    assert response.status_code == 201
    assert response.json['response'] == 'Expense created!'

def test_get_expense_by_id(test_client, init_database):
    '''
    DESCRIPTION: The endpoint to be tested Should return an expense with id 1

    TEST:
    ----
    GIVEN a Flask application configured for testing.
    WHEN the /expense/<int:id> endpoint receives a request.
    THEN check
        - that the status code returned is 200 indicating everything went OK
        - that the name in the response is the string "Expense 1"    
    '''
    #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = test_client.get('/expense/1',
                                headers = headers,
                                content_type = 'application/json')

    assert response.status_code == 200
    assert response.json['response']['name'] == 'Expense 1'

def test_get_list_expenses_by_owner(test_client, init_database):
    '''
    DESCRIPTION: The endpoint to be tested should return as list of expenses that belong to the logged user

    GIVEN a Flask application configured for testing.
    WHEN the /expense/list endpoint receives a request
    THEN check
        - that the status code returned is 200 indicating everything went OK
        - that the data type of the response is list
    '''
    #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = test_client.get('/expense/list',
                                headers = headers,
                                content_type = 'application/json')

    assert response.status_code == 200
    assert type(response.json['response']) == list

def test_delete_expense(test_client, init_database):
    '''
    DESCRIPTION: The endpoint to be tested should delete a specific expense identified by its id.

    TEST:
    ----
    GIVEN a Flask application configured for testing.
    WHEN the /expense/<int:id> receives a delete request.
    THEN check
        - that the status code returned is 204 indicating the item has been deleted.
    '''
    #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = test_client.delete('/expense/1',
                                headers = headers,
                                content_type = 'application/json')

    assert response.status_code == 204

def test_get_total_expense(test_client,init_database):
    '''
    DESCRIPTION: The endpoint to be tested should return the total expenses of the logged user
    
    TEST:
    ----
    GIVEN a Flask application configured for testing
    WHEN the /expense/total endpoint receives a get request.
    THEN check
        - that the status code returned is 200 indicating everything is OK
        - that the total returned is the same as the total obtained from the Expense model
    '''
    #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = test_client.get('/expense/total',
                                headers = headers,
                                content_type = 'application/json')

    #getting the total using the model
    expenses = ExpenseModel.find_expenses_by_owner(1)
    expenses_total = sum([exp.amount for exp in expenses])
    
    assert response.status_code == 200
    assert response.json['response'] == expenses_total

def test_get_total_expense_by_category(test_client, init_database):
    '''
    DESCRIPTION: The endpoint to be tested should return the total of expenses that belong to a especific 
    category, for this test the category wich name is "Category 1" will be used.

    TEST:
    ----
    GIVEN a Flask application configured for testing
    WHEN the /expense/total/<string:category_name> endpoint receives a get request.
    THEN check
        - That the status code returned is 200 indicating everything is OK
        - That the total expenses returned is the same as the total expenses obtained from the expense model
    '''
    #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = test_client.get('/expense/total/Category 1',
                                headers = headers,
                                content_type = 'application/json')

    #getting expenses from the model
    expenses = ExpenseModel.find_expenses_by_category(user_id=1, category_id=1)
    expenses_total = sum([exp.amount for exp in expenses])

    assert response.status_code == 200
    assert response.json['response'] == expenses_total

def test_get_list_expenses_by_category(test_client, init_database):
    '''
    DESCRIPTION: The endpoint to be tested should be a list of expenses that belong to a specific category
    for this test the category to be used will be the one identified with the string "Category 1"
    
    TEST
    ----
    GIVEN a Flask application configured for testing
    WHEN the /expense/list/<string:category_name> endpoint receives a get request
    THEN check
        - That the status code returned is 200 indicating everything went OK
        - That the data type of the response is list
    '''
    #login user
    response = test_client.post('/user/login',
                                data = json.dumps({'username':'user','password':'password1'}),
                                content_type = 'application/json')

    assert response.status_code == 200

    access_token = response.json["access_token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = test_client.get('/expense/list/Category 1',
                                headers = headers,
                                content_type = 'application/json')

    assert response.status_code == 200
    assert type(response.json['response']) == list
    


    






