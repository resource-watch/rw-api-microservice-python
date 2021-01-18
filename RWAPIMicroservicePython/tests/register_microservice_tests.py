import os

import pytest
import requests_mock
import json

import RWAPIMicroservicePython


@pytest.fixture
def validate_env():
    if not os.getenv('CT_URL'):
        raise Exception('CT_URL needs to be set')
    if not os.getenv('CT_TOKEN'):
        raise Exception('CT_TOKEN needs to be set')


@requests_mock.mock(kw='mocker')
def test_microservice_register(mocker):
    post_calls = mocker.post(os.getenv('CT_URL') + '/api/v1/microservice', status_code=204)

    RWAPIMicroservicePython.ct_register('test app', os.getenv('CT_URL'), 'http://local-url.com', True)

    assert post_calls.call_count == 1
    assert post_calls.called
    json_response = json.loads(post_calls.last_request.text)
    assert json_response['active'] is True
    assert json_response['url'] == u'http://local-url.com'
    assert json_response['name'] == u'test app'
