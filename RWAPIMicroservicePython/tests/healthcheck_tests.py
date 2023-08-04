import requests_mock
from flask import Flask
import RWAPIMicroservicePython
import boto3
from moto import mock_logs


@requests_mock.mock(kw='mocker')
@mock_logs()
def test_healthcheck(mocker):
    app = Flask(__name__)

    RWAPIMicroservicePython.register(
        app=app,
        gateway_url='https://gateway-url.com',
        token='microserviceToken',
        require_api_key=True,
        aws_region='us-east-1',
        aws_cloud_watch_log_stream_name='rw-api-microservice-python'
    )

    response = app.test_client().get('/healthcheck')
    assert response.status_code == 200
    assert response.data == b'ok'

    aws_mock = boto3.client('logs', region_name='us-east-1')
    log_lines = aws_mock.get_log_events(
        logGroupName="api-keys-usage",
        logStreamName="rw-api-microservice-python"
    )['events']
    assert len(log_lines) == 0
