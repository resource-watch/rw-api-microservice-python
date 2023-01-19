import pytest
import requests_mock
import json

import RWAPIMicroservicePython
from RWAPIMicroservicePython.errors import NotFound


def request_has_no_body(request):
    return request.text is None


def request_has_body(expected_body):
    def request_has_body_validator(request):
        return request.text == json.dumps(expected_body)
    return request_has_body_validator


@requests_mock.mock(kw='mocker')
def test_get_request_to_microservice_happy_case(mocker):
    get_calls = mocker.get('http://gateway-url.com/v1/microservice/endpoint', additional_matcher=request_has_no_body,
                           json={})

    RWAPIMicroservicePython.MICROSERVICE_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.GATEWAY_URL = 'http://gateway-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'GET',
        'uri': '/v1/microservice/endpoint'
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_delete_request_to_microservice_happy_case(mocker):
    get_calls = mocker.delete('http://gateway-url.com/v1/microservice/endpoint', additional_matcher=request_has_no_body,
                              json={})

    RWAPIMicroservicePython.MICROSERVICE_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.GATEWAY_URL = 'http://gateway-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'DELETE',
        'uri': '/v1/microservice/endpoint'
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_patch_request_to_microservice_happy_case(mocker):
    get_calls = mocker.patch('http://gateway-url.com/v1/microservice/endpoint', additional_matcher=request_has_body({'key': 'value'}), json={})

    RWAPIMicroservicePython.MICROSERVICE_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.GATEWAY_URL = 'http://gateway-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'PATCH',
        'uri': '/v1/microservice/endpoint',
        'body': {'key': 'value'}
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_put_request_to_microservice_happy_case(mocker):
    get_calls = mocker.put('http://gateway-url.com/v1/microservice/endpoint', additional_matcher=request_has_body({'key': 'value'}), json={})

    RWAPIMicroservicePython.MICROSERVICE_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.GATEWAY_URL = 'http://gateway-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'PUT',
        'uri': '/v1/microservice/endpoint',
        'body': {'key': 'value'}
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_post_request_to_microservice_happy_case(mocker):
    get_calls = mocker.post('http://gateway-url.com/v1/microservice/endpoint', additional_matcher=request_has_body({'key': 'value'}), json={})

    RWAPIMicroservicePython.MICROSERVICE_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.GATEWAY_URL = 'http://gateway-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'POST',
        'uri': '/v1/microservice/endpoint',
        'body': {'key': 'value'}
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_no_api_version(mocker):
    get_calls = mocker.get('http://gateway-url.com/microservice/endpoint', json={})

    RWAPIMicroservicePython.MICROSERVICE_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.GATEWAY_URL = 'http://gateway-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'GET',
        'uri': '/microservice/endpoint'
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_ct_404(mocker):
    get_calls = mocker.get('http://gateway-url.com/v1/microservice/endpoint', status_code=404, json={
        "errors": [
            {
                "status": 404,
                "detail": "Endpoint not found"
            }
        ]
    })

    RWAPIMicroservicePython.MICROSERVICE_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.GATEWAY_URL = 'http://gateway-url.com'

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'GET',
        'uri': '/v1/microservice/endpoint'
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {'errors': [{'detail': 'Endpoint not found', 'status': 404}]}


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_http_404(mocker):
    get_calls = mocker.get('http://gateway-url.com/v1/microservice/endpoint', status_code=404)

    RWAPIMicroservicePython.MICROSERVICE_TOKEN = 'microserviceToken'
    RWAPIMicroservicePython.GATEWAY_URL = 'http://gateway-url.com'

    with pytest.raises(NotFound) as e:
        assert RWAPIMicroservicePython.request_to_microservice({
            'method': 'GET',
            'uri': '/v1/microservice/endpoint'
        })

        assert e.message == ''

    assert get_calls.call_count == 1
    assert get_calls.called
