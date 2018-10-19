from initialize import create_app
import pytest
from app import Todo, TodoList

@pytest.fixture
def app():
    app, api = create_app()
    api.add_resource(TodoList, '/todosList')
    api.add_resource(Todo, '/todosList/<todo_id>')
    return app

def test_Get_Item(client):
    result = client.get('/todosList/todo1')
    assert result.status_code == 200

def test_Delete(client):
    result = client.delete('/todosList/todo2')
    assert result.status_code == 204

def test_Put(client):
    payload = {'title': 'unittest'}
    result = client.put('todosList/todo1', data=payload)
    assert result.status_code == 200

def test_Get_All(client):
    result = client.get('todosList')
    assert result.status_code == 200

def test_Post(client):
    payload = {'title': 'new_title', 'due_date': '01/01/2020', 'completed': True}
    result = client.post('todosList', data=payload)
    assert result.status_code == 201
