import json
import requests_mock
from RWAPIMicroservicePython.tests.mocks import mock_request_validation
from flask import Flask, Blueprint, request

import RWAPIMicroservicePython


@requests_mock.mock(kw='mocker')
def test_cors_headers_are_present(mocker):
    get_user_data_calls = mock_request_validation(mocker, user=None)
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
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    response = app.test_client().put('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    response = app.test_client().post('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    response = app.test_client().patch('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    response = app.test_client().delete('/test', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

