import json

import requests_mock
from flask import Flask, Blueprint, request

import RWAPIMicroservicePython


@requests_mock.mock(kw='mocker')
def test_inject_logged_user(mocker):
    get_user_data_calls = mocker.get('http://ct-url.com/auth/user/me',
                                     request_headers={'Authorization': 'Bearer abcd'},
                                     status_code=200,
                                     json={
                                         'id': '1a10d7c6e0a37126611fd7a7',
                                         'name': 'test admin',
                                         'role': 'ADMIN',
                                         'provider': 'local',
                                         'email': 'user@control-tower.org',
                                         'extraUserData': {
                                             'apps': [
                                                 'rw',
                                                 'gfw',
                                                 'gfw-climate',
                                                 'prep',
                                                 'aqueduct',
                                                 'forest-atlas',
                                                 'data4sdgs'
                                             ]
                                         }
                                     })

    test_endpoints = Blueprint('rw_api', __name__)

    @test_endpoints.route('/test', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
    def test_route():
        logged_user = json.loads(request.args.get("loggedUser", '{}'))
        assert logged_user.get('name') == 'test admin'
        assert logged_user.get('role') == 'ADMIN'
        assert logged_user.get('provider') == 'local'
        assert logged_user.get('email') == 'user@control-tower.org'
        assert logged_user.get('extraUserData').get('apps') == [
            'rw',
            'gfw',
            'gfw-climate',
            'prep',
            'aqueduct',
            'forest-atlas',
            'data4sdgs'
        ]
        return 'ok', 200

    app = Flask(__name__)

    app.register_blueprint(test_endpoints)

    RWAPIMicroservicePython.register(
        app=app,
        name='test app',
        info={},
        swagger={},
        mode=RWAPIMicroservicePython.NORMAL_MODE,
        ct_url='http://ct-url.com',
        url='http://local-url.com',
        delay=None,
        api_version='v1',
        token='microserviceToken'
    )

    response = app.test_client().get('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().put('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().post('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().patch('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().delete('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 200
    assert response.data == b'ok'

    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 5


@requests_mock.mock(kw='mocker')
def test_inject_logged_user_when_no_authorization_header_is_present(mocker):
    # This is never actually called, were just using it as a way to validate that no calls are made to this endpoint
    get_user_data_calls = mocker.get('http://ct-url.com/auth/user/me', status_code=200, json={})

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
        name='test app',
        info={},
        swagger={},
        mode=RWAPIMicroservicePython.NORMAL_MODE,
        ct_url='http://ct-url.com',
        url='http://local-url.com',
        delay=None,
        api_version='v1',
        token='microserviceToken'
    )

    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().put('/test')
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().post('/test')
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().patch('/test')
    assert response.status_code == 200
    assert response.data == b'ok'

    response = app.test_client().delete('/test')
    assert response.status_code == 200
    assert response.data == b'ok'

    assert not get_user_data_calls.called
    assert get_user_data_calls.call_count == 0


@requests_mock.mock(kw='mocker')
def test_inject_logged_user_when_token_is_invalid(mocker):
    get_user_data_calls = mocker.get('http://ct-url.com/auth/user/me',
                                     request_headers={'Authorization': 'Bearer abcd'},
                                     status_code=401,
                                     json={
                                         "errors": [
                                             {
                                                 "status": 401,
                                                 "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."
                                             }
                                         ]
                                     })

    test_endpoints = Blueprint('rw_api', __name__)

    @test_endpoints.route('/test', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
    def test_route():
        raise Exception('Tests should never reach this point');

    app = Flask(__name__)

    app.register_blueprint(test_endpoints)

    RWAPIMicroservicePython.register(
        app=app,
        name='test app',
        info={},
        swagger={},
        mode=RWAPIMicroservicePython.NORMAL_MODE,
        ct_url='http://ct-url.com',
        url='http://local-url.com',
        delay=None,
        api_version='v1',
        token='microserviceToken'
    )

    response = app.test_client().get('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 401
    assert response.json == json.loads(b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    response = app.test_client().put('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 401
    assert response.json == json.loads(b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    response = app.test_client().post('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 401
    assert response.json == json.loads(b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    response = app.test_client().patch('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 401
    assert response.json == json.loads(b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    response = app.test_client().delete('/test', headers={'Authorization': 'Bearer abcd'})
    assert response.status_code == 401
    assert response.json == json.loads(b'{"errors": [{"status": 401, "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."}]}')

    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 5
