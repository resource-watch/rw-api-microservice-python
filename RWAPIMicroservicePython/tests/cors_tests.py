import json
import requests_mock
from RWAPIMicroservicePython.tests.mocks import mock_request_validation
from flask import Flask, Blueprint, request
import boto3
from moto import mock_logs
import RWAPIMicroservicePython


@requests_mock.mock(kw='mocker')
@mock_logs()
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
        aws_region='us-east-1',
        aws_cloud_watch_log_stream_name='rw-api-microservice-python'
    )

    response = app.test_client().get('/test?foo=bar', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    response = app.test_client().put('/test?foo=bar', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    response = app.test_client().post('/test?foo=bar', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    response = app.test_client().patch('/test?foo=bar', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    response = app.test_client().delete('/test?foo=bar', headers={'x-api-key': 'api-key-test'})
    assert response.status_code == 200
    assert response.data == b'ok'
    assert response.headers['access-control-allow-origin'] == '*'
    assert response.headers['access-control-allow-headers'] == 'upgrade-insecure-requests'
    assert response.headers['access-control-allow-credentials'] == 'true'
    assert response.headers['access-control-allow-methods'] == 'OPTIONS,GET,PUT,POST,PATCH,DELETE'

    aws_mock = boto3.client('logs', region_name='us-east-1')
    log_lines = aws_mock.get_log_events(
        logGroupName="api-keys-usage",
        logStreamName="rw-api-microservice-python"
    )['events']
    assert len(log_lines) == 5
    assert log_lines[0]['message'] == '{"request": {"method": "GET", "path": "/test", "query": {"foo": "bar"}}, "loggedUser": {"id": "anonymous", "name": "anonymous", "role": "anonymous", "provider": "anonymous"}, "requestApplication": {"id": "649c4b204967792f3a4e52c9", "name": "grouchy-armpit", "organization": null, "user": null, "apiKeyValue": "api-key-test"}}'
    assert log_lines[1]['message'] == '{"request": {"method": "PUT", "path": "/test", "query": {"foo": "bar"}}, "loggedUser": {"id": "anonymous", "name": "anonymous", "role": "anonymous", "provider": "anonymous"}, "requestApplication": {"id": "649c4b204967792f3a4e52c9", "name": "grouchy-armpit", "organization": null, "user": null, "apiKeyValue": "api-key-test"}}'
    assert log_lines[2]['message'] == '{"request": {"method": "POST", "path": "/test", "query": {"foo": "bar"}}, "loggedUser": {"id": "anonymous", "name": "anonymous", "role": "anonymous", "provider": "anonymous"}, "requestApplication": {"id": "649c4b204967792f3a4e52c9", "name": "grouchy-armpit", "organization": null, "user": null, "apiKeyValue": "api-key-test"}}'
    assert log_lines[3]['message'] == '{"request": {"method": "PATCH", "path": "/test", "query": {"foo": "bar"}}, "loggedUser": {"id": "anonymous", "name": "anonymous", "role": "anonymous", "provider": "anonymous"}, "requestApplication": {"id": "649c4b204967792f3a4e52c9", "name": "grouchy-armpit", "organization": null, "user": null, "apiKeyValue": "api-key-test"}}'
    assert log_lines[4]['message'] == '{"request": {"method": "DELETE", "path": "/test", "query": {"foo": "bar"}}, "loggedUser": {"id": "anonymous", "name": "anonymous", "role": "anonymous", "provider": "anonymous"}, "requestApplication": {"id": "649c4b204967792f3a4e52c9", "name": "grouchy-armpit", "organization": null, "user": null, "apiKeyValue": "api-key-test"}}'

