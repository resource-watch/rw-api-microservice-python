from flask import Flask, Blueprint
import RWAPIMicroservicePython
from moto import mock_logs


@mock_logs()
def test_cache_headers_set_to_private():
    test_endpoints = Blueprint('rw_api', __name__)

    @test_endpoints.route('/test', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
    def test_route():
        return 'ok', 200

    app = Flask(__name__)

    app.register_blueprint(test_endpoints)

    RWAPIMicroservicePython.register(
        app=app,
        gateway_url='http://gateway-url.com',
        token='microserviceToken',
        require_api_key=True,
        aws_region='us-east-1',
        aws_cloud_watch_log_stream_name='rw-api-microservice-python'
    )

    response = app.test_client().get('/test', headers={'x-api-key': 'api-key-test'})
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'

    response = app.test_client().put('/test', headers={'x-api-key': 'api-key-test'})
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'

    response = app.test_client().post('/test', headers={'x-api-key': 'api-key-test'})
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'

    response = app.test_client().patch('/test', headers={'x-api-key': 'api-key-test'})
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'

    response = app.test_client().delete('/test', headers={'x-api-key': 'api-key-test'})
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'
