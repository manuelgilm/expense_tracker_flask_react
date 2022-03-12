from http.client import ResponseNotReady
import json
from src.models.expense import ExpenseModel

def test_create_expense(test_client, init_database):
    '''
    DOC
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
    DOC
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
    assert response.json['name'] == 'Expense 1'

def test_get_list_expenses_by_owner(test_client, init_database):
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
    response = test_client.get('/expense/list',
                                headers = headers,
                                content_type = 'application/json')

    assert response.status_code == 200
    assert type(response.json['response']) == list

def test_delete_expense(test_client, init_database):
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
    response = test_client.delete('/expense/1',
                                headers = headers,
                                content_type = 'application/json')

    assert response.status_code == 204

def test_get_total_expense(test_client,init_database):
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
    DOC
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
    DOC
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
    


    






