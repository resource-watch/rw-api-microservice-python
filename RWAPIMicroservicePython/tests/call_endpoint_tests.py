import os

import pytest
import requests_mock

import RWAPIMicroservicePython
from RWAPIMicroservicePython.errors import NotFound


@pytest.fixture
def validate_env():
    if not os.getenv('CT_URL'):
        raise Exception('CT_URL needs to be set')
    if not os.getenv('CT_TOKEN'):
        raise Exception('CT_TOKEN needs to be set')


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_happy_case(mocker):
    get_calls = mocker.get(os.getenv('CT_URL') + '/microservice/endpoint', json={})

    response = RWAPIMicroservicePython.request_to_microservice({
        'method': 'GET',
        'uri': '/microservice/endpoint'
    })

    assert get_calls.call_count == 1
    assert get_calls.called

    assert response == {}


@requests_mock.mock(kw='mocker')
def test_request_to_microservice_ct_404(mocker):
    get_calls = mocker.get(os.getenv('CT_URL') + '/microservice/endpoint', status_code=404, json={
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
    get_calls = mocker.get(os.getenv('CT_URL') + '/microservice/endpoint', status_code=404)

    with pytest.raises(NotFound) as e:
        assert RWAPIMicroservicePython.request_to_microservice({
            'method': 'GET',
            'uri': '/microservice/endpoint'
        })

        assert e.message == ''
