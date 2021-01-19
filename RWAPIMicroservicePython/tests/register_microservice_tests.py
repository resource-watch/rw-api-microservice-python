import json
import os

import pytest
import requests_mock
from flask import Flask

import RWAPIMicroservicePython


@pytest.fixture
def validate_env():
    if not os.getenv('CT_URL'):
        raise Exception('CT_URL needs to be set')
    if not os.getenv('CT_TOKEN'):
        raise Exception('CT_TOKEN needs to be set')


@requests_mock.mock(kw='mocker')
def test_microservice_register_no_register(mocker):
    post_calls = mocker.post(os.getenv('CT_URL') + '/api/v1/microservice', status_code=204)

    app = Flask(__name__)

    RWAPIMicroservicePython.register(
        app=app,
        name='test app',
        info={},
        swagger={},
        mode=RWAPIMicroservicePython.NORMAL_MODE,
        ct_url=os.getenv('CT_URL'),
        url='http://local-url.com',
        delay=None
    )

    assert post_calls.call_count == 0


@requests_mock.mock(kw='mocker')
def test_microservice_register_no_register(mocker):
    post_calls = mocker.post(os.getenv('CT_URL') + '/api/v1/microservice', status_code=204)

    app = Flask(__name__)

    RWAPIMicroservicePython.register(
        app=app,
        name='test app',
        info={},
        swagger={},
        mode=RWAPIMicroservicePython.AUTOREGISTER_MODE,
        ct_url=os.getenv('CT_URL'),
        url='http://local-url.com',
        delay=None
    )

    assert post_calls.call_count == 1
    assert post_calls.called
    json_response = json.loads(post_calls.last_request.text)
    assert json_response['active'] is True
    assert json_response['url'] == u'http://local-url.com'
    assert json_response['name'] == u'test app'
