import pytest
from app import app as flask_app
from app import get_db

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['DATABASE'] = ':memory:'
    with flask_app.app_context():
        db = get_db()
        db.execute('CREATE TABLE resources (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, quantity INTEGER NOT NULL)')
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_resources(client):
    response = client.get('/resources')
    assert response.status_code == 200
    assert response.json == []

def test_create_resource(client):
    response = client.post('/resources', json={'name': 'Water', 'quantity': 100})
    assert response.status_code == 201
    assert response.json['name'] == 'Water'
    assert response.json['quantity'] == 100

    response = client.get('/resources')
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Water'

# Add more tests for update and delete as needed