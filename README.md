# RW API microservice utility for Python+Flask applications

[![Build Status](https://travis-ci.com/resource-watch/rw-api-microservice-python.svg?branch=main)](https://travis-ci.com/resource-watch/rw-api-microservice-python)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fe857a0082ab7d0bbd64/test_coverage)](https://codeclimate.com/github/resource-watch/rw-api-microservice-python/test_coverage)

Library to register and integrate microservices in the [RW API](https://api.resourcewatch.org/).

## Requirements

This library is tested to work with following Python versions:

- 3.11.4
- 3.10.12

Additionally, it requires the following Python libraries:

- Flask (tested with v2.2 and v2.3)
- requests
- boto3

This library includes testing helpers for your code, in which case you will also need:

- requests_mock
- moto (not required but recommended)

## Install

```shell
pip install RWAPIMicroservicePython
```

## Testing

```shell
tox
```

These tests run on multiple python versions in parallel. You may want/need to use something like `pyenv` to support the
underlying version handling. If you are using `pyenv virtualenv` be sure to deactivate any envs before calling `tox`.

## Use in microservice

To bootstrap your microservice, use:

```python
import RWAPIMicroservicePython
from flask import Flask

app = Flask(__name__)

RWAPIMicroservicePython.register(
    app=app,
    gateway_url='https://control-tower.your.domain',
    token='microserviceTokenForControlTower',
    aws_cloud_watch_log_stream_name='nameOfTheAWSCloudwatchLogStream',
    aws_region='youAWSRegion'
)
```

This will add pre- and post-request hooks to your Flask application lifecycle.
The pre-request hook will validate authentication and API key. For more details, check the RW API docs. It will also log
request data to AWS CloudWatch for analytics and usage evaluation purposes.
The post-request hook will add CORS headers to the response.

The library also includes a utility function to simplify making a request to another microservice:

```python
from RWAPIMicroservicePython import request_to_microservice


def execute():
    config = {
        'uri': '/v1/dataset/1234',
        'method': 'POST',
        'api_key': '<api key from the request>',
        'body': {'key': 'value'}
    }
    response = request_to_microservice(**config)
    if not response or response.get('errors'):
        raise Exception(message='Dataset not found')

    dataset = response.get('data', None).get('attributes', None)
    return dataset
```

All arguments except the body are required.

## Configuration

These are the values you'll need to provide when using this library:

See [this link](https://docs.fastly.com/en/guides/finding-and-managing-your-account-info) for details on how to get
Fastly credentials.

| Argument name                   | Type           | Description                                                                                               | Required? | Default value    |
|---------------------------------|----------------|-----------------------------------------------------------------------------------------------------------|-----------|------------------|
| app                             | `Flask` object | The [Flask](https://flask.palletsprojects.com) `app`                                                      | yes       |                  |
| token                           | string         | JWT token to use on calls to other services                                                               | yes       |                  |
| require_api_key                 | boolean        | If API keys are required. If set to true, requests with no API key automatically get a HTTP 403 response. | no        | true             |
| aws_cloud_watch_logging_enabled | boolean        | If API key usage should be logged to AWS CloudWatch.                                                      | no        | true             |
| aws_region                      | string         | Which AWS region to use when logging requests to AWS CloudWatch.                                          | yes       |                  |
| aws_cloud_watch_log_group_name  | string         | Which CloudWatch Log Group name to use when logging requests to AWS CloudWatch.                           | no        | 'api-keys-usage' |
| aws_cloud_watch_log_stream_name | string         | Which CloudWatch Log Stream name to use when logging requests to AWS CloudWatch.                          | yes       |                  |

## Testing your microservices

Besides the functionality above, this library also includes testing utility functions to help you add e2e testing
to your RW API microservices. In order to use these utility functions, you must have installed and configured the
`requests_mock` library on your project (see `setup.py` to learn exactly which version is officially supported).

```python
from RWAPIMicroservicePython.test_utils import mock_request_validation
from your_application import create_flask_application
import requests_mock
import unittest


class ExampleTest(unittest.TestCase):

    def setUp(self):
        app = create_flask_application()
        app.config.update({
            "TESTING": True,
        })
        self.app = app.test_client()

    @requests_mock.mock(kw='mocker')
    def test_some_method(self, mocker):
        """test geostore error message"""
        mock_request_validation(mocker)

        response = self.app.get('/some/endpoint')

        self.assertEqual(response.status_code, 200)
```

The example above illustrates how you can use the `mock_request_validation` helper function to mock the call made by
this library to load the application and user data from the RW API.

Since this library also makes per-request calls to AWS CloudWatch, you may also wish to mock those calls when creating
your tests. To do so, we recommend using the `moto` library. You can find examples of its usage in
the `RWAPIMicroservicePython/tests` folder.