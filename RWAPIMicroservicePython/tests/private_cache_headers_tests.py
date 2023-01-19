from flask import Flask, Blueprint

import RWAPIMicroservicePython


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
        token='microserviceToken'
    )

    response = app.test_client().get('/test')
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'

    response = app.test_client().put('/test')
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'

    response = app.test_client().post('/test')
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'

    response = app.test_client().patch('/test')
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'

    response = app.test_client().delete('/test')
    assert 'cache-control' in response.headers
    assert response.headers.get('cache-control') == 'private'
