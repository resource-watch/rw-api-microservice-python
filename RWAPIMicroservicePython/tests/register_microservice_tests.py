import json
import os

import requests_mock
from flask import Flask

import RWAPIMicroservicePython


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
        ct_url='http://ct-url.com',
        url='http://local-url.com',
        delay=None,
        api_version='v1',
        token='microserviceToken'
    )

    assert post_calls.call_count == 0


@requests_mock.mock(kw='mocker')
def test_microservice_register_no_register(mocker):
    post_calls = mocker.post('http://ct-url.com/api/v1/microservice', status_code=204)

    app = Flask(__name__)

    RWAPIMicroservicePython.register(
        app=app,
        name='test app',
        info={},
        swagger={},
        mode=RWAPIMicroservicePython.AUTOREGISTER_MODE,
        ct_url='http://ct-url.com',
        url='http://local-url.com',
        delay=None,
        api_version='v1',
        token='microserviceToken'
    )

    assert post_calls.call_count == 1
    assert post_calls.called
    json_response = json.loads(post_calls.last_request.text)
    assert json_response['active'] is True
    assert json_response['url'] == u'http://local-url.com'
    assert json_response['name'] == u'test app'
