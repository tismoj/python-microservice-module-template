from api import api
from flask import request
import pytest
import flask


@pytest.fixture
def api_client():
    client = api.app.test_client()
    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    api.app.config['TESTING'] = True
    api.CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}

    # Establish an application context before running the tests.
    app_context = api.app.app_context()
    app_context.push()

    yield client

    app_context.pop()


def test_hello(api_client):
    """
    GIVEN a Flask application
    WHEN the '/hello/' page is requested (POST) and given a name member in the JSON payload
    THEN that name's value should appear in the returned string
    """
    response = api_client.post('/hello/', json={
        'name': 'Flask'
    })
    assert response.status_code == 200
    assert b'Hello, Flask!' in response.data


def test_hello2(api_client):
    """
    GIVEN a Flask application
    WHEN the '/hello2/<name>' page is requested (GET) and given a name argument
    THEN that name argument should appear in the returned string
    """
    response = api_client.get('/hello2/Flask')
    assert response.status_code == 200
    assert b'Hello, Flask!' in response.data

    with api.app.test_request_context('/hello2/Flask?name=some_name'):
        assert flask.request.path == '/hello2/Flask'
        assert flask.request.args['name'] == 'some_name'

    with api.app.test_client() as c:
        rv = c.get('/hello2/Flask?name=some_other_name')
        assert request.path == '/hello2/Flask'
        assert request.args['name'] == 'some_other_name'
        assert rv.status_code == 200
        assert b'Hello, Flask!' in rv.data

