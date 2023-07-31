import json
from RWAPIMicroservicePython.tests.mocks import mock_request_validation, mock_request_validation_invalid_token
from RWAPIMicroservicePython.tests.constants import USER
import requests_mock
from flask import Flask, Blueprint, request

import RWAPIMicroservicePython


@requests_mock.mock(kw='mocker')
def test_inject_logged_user(mocker):
    get_user_data_calls = mock_request_validation(mocker)

    test_endpoints = Blueprint('rw_api', __name__)

    @test_endpoints.route('/test', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
    def test_route():
        logged_user = json.loads(request.args.get("loggedUser", '{}'))
        assert logged_user.get('name') == USER['name']
        assert logged_user.get('role') == USER['role']
        assert logged_user.get('provider') == USER['provider']
        assert logged_user.get('email') == USER['email']
        assert logged_user.get('extraUserData').get('apps') == USER['extraUserData']['apps']
        return 'ok', 200

    app = Flask(__name__)

    app.register_blueprint(test_endpoints)

    RWAPIMicroservicePython.register(
        app=app,
        gateway_url='http://gateway-url.com',
        token='microserviceToken',
        require_api_key=True
    )

    response = app.test_client().get('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().put('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().post('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().patch('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().delete('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 5


@requests_mock.mock(kw='mocker')
def test_inject_logged_user_when_no_authorization_header_is_present(mocker):
    # This is never actually called, were just using it as a way to validate that no calls are made to this endpoint
    get_user_data_calls = mock_request_validation(mocker, user=None, application=None)

    test_endpoints = Blueprint('rw_api', __name__)

    @test_endpoints.route('/test', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
    def test_route():
        logged_user = json.loads(request.args.get("loggedUser", '{}'))
        assert logged_user == {}
        return 'ok', 200

    app = Flask(__name__)

    app.register_blueprint(test_endpoints)

    RWAPIMicroservicePython.register(
        app=app,
        gateway_url='http://gateway-url.com',
        token='microserviceToken',
        require_api_key=True
    )

    response = app.test_client().get('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().put('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().post('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().patch('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().delete('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'

    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 5


@requests_mock.mock(kw='mocker')
def test_inject_logged_user_when_token_is_invalid(mocker):
    get_user_data_calls = mock_request_validation_invalid_token(mocker)

    test_endpoints = Blueprint('rw_api', __name__)

    @test_endpoints.route('/test', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
    def test_route():
        raise Exception('Tests should never reach this point');

    app = Flask(__name__)

    app.register_blueprint(test_endpoints)

    RWAPIMicroservicePython.register(
        app=app,
        gateway_url='http://gateway-url.com',
        token='microserviceToken',
        require_api_key=True
    )

    response = app.test_client().get('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 401
    assert response.json == json.loads(
        b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    response = app.test_client().put('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 401
    assert response.json == json.loads(
        b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    response = app.test_client().post('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 401
    assert response.json == json.loads(
        b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    response = app.test_client().patch('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 401
    assert response.json == json.loads(
        b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    response = app.test_client().delete('/test', headers={'Authorization': 'Bearer abcd', 'x-api-key': 'api-key-test'})
    assert response.status_code == 401
    assert response.json == json.loads(
        b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 5
