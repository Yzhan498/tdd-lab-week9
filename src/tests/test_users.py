# src/tests/test_users.py 
import json 
from src.api.models import User
def test_add_user(test_app, test_database): 
    client = test_app.test_client() 
    resp = client.post( 
        '/users', 
        data=json.dumps({ 
            'username': 'john', 
            'email': 'john@algonquincollege.com' 
        }), 
        content_type='application/json', 
    ) 
    data = json.loads(resp.data.decode()) 
    assert resp.status_code == 201 
    assert 'john@algonquincollege.com was added!' in data['message']

def test_add_user_invalid_json(test_app, test_database): 
    client = test_app.test_client() 
    resp = client.post( 
        '/users', 
        data=json.dumps({}), 
        content_type='application/json', 
    ) 
    data = json.loads(resp.data.decode()) 
    assert resp.status_code == 400 
    assert 'Input payload validation failed' in data['message'] 
def test_add_user_invalid_json_keys(test_app, test_database): 
    client = test_app.test_client() 
    resp = client.post( 
        '/users', 
        data=json.dumps({"email": "john@testdriven.io"}), 
        content_type='application/json', 
    ) 
    data = json.loads(resp.data.decode()) 
    assert resp.status_code == 400 
    assert 'Input payload validation failed' in data['message'] 
def test_add_user_duplicate_email(test_app, test_database): 
    client = test_app.test_client() 
    client.post( 
        '/users', 
        data=json.dumps({ 
            'username': 'john', 
            'email': 'john@algonquincollege.com' 
        }), 
        content_type='application/json', 
    ) 
    resp = client.post( 
        '/users', 
        data=json.dumps({ 
            'username': 'john', 
            'email': 'john@algonquincollege.com' 
        }), 
        content_type='application/json', 
    ) 
    data = json.loads(resp.data.decode()) 
    assert resp.status_code == 400 
    assert 'Sorry. That email already exists.' in data['message'] 

def test_single_user(test_app, test_database, add_user): 
    user = add_user('jeffrey', 'jeffrey@testdriven.io') 
    client = test_app.test_client() 
    resp = client.get(f'/users/{user.id}') 
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200 
    assert 'jeffrey' in data['username'] 
    assert 'jeffrey@testdriven.io' in data['email'] 

def test_single_user_incorrect_id(test_app, test_database, add_user): 
    user = add_user('jeffrey', 'jeffrey@testdriven.io')
    client = test_app.test_client() 
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode()) 
    assert resp.status_code == 200 
    assert 'jeffrey' in data['username'] 
    assert 'jeffrey@testdriven.io' in data['email']
def test_all_users(test_app, test_database, add_user): 
    test_database.session.query(User).delete() # new
    add_user('john', 'john@algonquincollege.com') 
    add_user('fletcher', 'fletcher@notreal.com') 
    client = test_app.test_client() 
    resp = client.get('/users') 
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'john' in data[0]['username'] 
    assert 'john@algonquincollege.com' in data[0]['email'] 
    assert 'fletcher' in data[1]['username'] 
    assert 'fletcher@notreal.com' in data[1]['email'] 

def test_put(test_app, test_database, add_user):
    # Create a test user
    user = add_user('test_user', 'test@example.com')
    
    # Data for the update
    new_username = 'updated_username'
    new_email = 'updated_email@example.com'

    # Send a PUT request to update the user
    client = test_app.test_client()
    resp = client.put(
        f'/users/{user.id}',
        data=json.dumps({
            'username': new_username,
            'email': new_email
        }),
        content_type='application/json'
    )

    # Check the response status code
    assert resp.status_code == 200

    # Retrieve the updated user from the database
    updated_user = User.query.get(user.id)

    # Check if the user was updated successfully
    assert updated_user.username == new_username
    assert updated_user.email == new_email

def test_delete_user(test_app, test_database, add_user):
    # Create a test user
    user = add_user('user_to_delete', 'delete@example.com')
    
    # Send a DELETE request to remove the user
    client = test_app.test_client()
    resp = client.delete(f'/users/{user.id}')
    
    # Check the response status code
    assert resp.status_code == 200
    
    # Check if the user was deleted successfully
    deleted_user = User.query.get(user.id)
    assert deleted_user is None 
