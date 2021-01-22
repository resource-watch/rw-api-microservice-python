import pytest
import requests_mock

import RWAPIMicroservicePython
from RWAPIMicroservicePython.errors import NotFound


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_happy_case(mocker):
    get_calls = mocker.get('http://ct-url.com/v1/microservice/endpoint', json={})

    RWAPIMicroservicePython.API_VERSION = 'v1'
    RWAPIMicroservicePython.CT_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.CT_URL = 'http://ct-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'GET',
        'uri': '/microservice/endpoint'
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_no_api_version(mocker):
    get_calls = mocker.get('http://ct-url.com/microservice/endpoint', json={})

    RWAPIMicroservicePython.API_VERSION = None
    RWAPIMicroservicePython.CT_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.CT_URL = 'http://ct-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'GET',
        'uri': '/microservice/endpoint'
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_ct_404(mocker):
    get_calls = mocker.get('http://ct-url.com/v1/microservice/endpoint', status_code=404, json={
        "errors": [
            {
                "status": 404,
                "detail": "Endpoint not found"
            }
        ]
    })

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'GET',
        'uri': '/microservice/endpoint'
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {'errors': [{'detail': 'Endpoint not found', 'status': 404}]}


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_http_404(mocker):
    get_calls = mocker.get('http://ct-url.com/v1/microservice/endpoint', status_code=404)

    with pytest.raises(NotFound) as e:
        assert RWAPIMicroservicePython.request_to_microservice({
            'method': 'GET',
            'uri': '/microservice/endpoint'
        })

        assert e.message == ''

    assert get_calls.call_count == 1
    assert get_calls.called
