import json
import requests
import logging
from flask import request, jsonify, Response
from requests import Session, Request
from werkzeug.datastructures import ImmutableMultiDict

from RWAPIMicroservicePython.errors import NotFound, ApiKeyError, ValidationError
from RWAPIMicroservicePython.cloudwatch import CloudWatchService

GATEWAY_URL: str = ''
MICROSERVICE_TOKEN: str = ''


def register(
        app,
        gateway_url: str,
        token: str,
        aws_region: str,
        aws_cloud_watch_log_stream_name: str,
        require_api_key=True,
        aws_cloud_watch_logging_enabled=True,
        aws_cloud_watch_log_group_name: str = 'api-keys-usage',
):
    global MICROSERVICE_TOKEN, GATEWAY_URL
    MICROSERVICE_TOKEN = token
    GATEWAY_URL = gateway_url

    cloud_watch_service = CloudWatchService(aws_region, aws_cloud_watch_log_group_name, aws_cloud_watch_log_stream_name)

    @app.after_request
    def set_cors_headers(response):
        response.headers["access-control-allow-origin"] = "*"
        response.headers["access-control-allow-headers"] = "upgrade-insecure-requests"
        response.headers["access-control-allow-credentials"] = "true"
        response.headers["access-control-allow-methods"] = "OPTIONS,GET,PUT,POST,PATCH,DELETE"
        return response

    @app.before_request
    def before_request():
        try:
            request_validation_data = get_logger_user()
        except ApiKeyError:
            return jsonify({'errors': {'message': 'Required API key not found', 'code': 403}}), 403
        except ValidationError as e:
            return Response(e.message, status=e.code, mimetype='application/json')
        except Exception as e:
            return e

        if aws_cloud_watch_logging_enabled:
            log_request_to_cloud_watch(request_validation_data)

        inject_request_validation_data(request_validation_data)

    def log_request_to_cloud_watch(request_validation_data):
        logging.debug('[log_request_to_cloud_watch] Logging request to CloudWatch')

        log_query = request.args.copy()
        if 'loggedUser' in log_query:
            del log_query['loggedUser']
        log_content = {
            'request': {
                'method': request.method,
                'path': request.path,
                'query': log_query,
            }
        }

        if 'user' in request_validation_data and 'data' in request_validation_data['user']:
            user_data = request_validation_data['user']['data']
            if user_data['id'] == 'microservice':
                log_content['loggedUser'] = {
                    'id': user_data['id'],
                }
            else:
                log_content['loggedUser'] = {
                    'id': user_data['id'],
                    'name': user_data['name'],
                    'role': user_data['role'],
                    'provider': user_data['provider'],
                }
        else:
            log_content['loggedUser'] = {
                'id': 'anonymous',
                'name': 'anonymous',
                'role': 'anonymous',
                'provider': 'anonymous',
            }

        if 'application' in request_validation_data and 'data' in request_validation_data['application']:
            application_data = request_validation_data['application']['data']
            log_content['requestApplication'] = {
                'id': application_data['id'],
                'name': application_data['attributes']['name'],
                'organization': application_data['attributes']['organization'],
                'user': application_data['attributes']['user'],
                'apiKeyValue': application_data['attributes']['apiKeyValue'],
            }
        else:
            log_content['requestApplication'] = {
                'id': 'anonymous',
                'name': 'anonymous',
                'organization': None,
                'user': None,
                'apiKeyValue': None,
            }

        cloud_watch_service.log_to_cloud_watch(json.dumps(log_content))

    def inject_request_validation_data(request_validation_data):
        http_args = request.args.to_dict()

        if 'user' in request_validation_data and 'data' in request_validation_data['user']:
            http_args['loggedUser'] = json.dumps(request_validation_data['user']['data'])
        else:
            http_args['loggedUser'] = '{}'
        request.args = ImmutableMultiDict(http_args)

    def get_logger_user():
        if 'x-api-key' not in request.headers and require_api_key:
            raise ApiKeyError('Required API key not found')

        body = {}

        if 'authorization' in request.headers:
            body['userToken'] = request.headers['authorization']

        if 'x-api-key' in request.headers:
            body['apiKey'] = request.headers['x-api-key']

        if body:
            logged_user_response = requests.post(
                GATEWAY_URL + '/v1/request/validate',
                headers={
                    'content-type': 'application/json',
                    'authorization': f"Bearer {MICROSERVICE_TOKEN}"
                },
                data=body
            )

            if logged_user_response.status_code >= 400:
                raise ValidationError(message=logged_user_response.text, code=logged_user_response.status_code)

            # http_args = request.args.to_dict()
            # http_args['loggedUser'] = logged_user_response.text
            # request.args = ImmutableMultiDict(http_args)

            return logged_user_response.json()
        else:
            return {}

    @app.after_request
    def add_cache_headers(response):
        response.headers.set('cache-control', 'private')
        return response


def request_to_microservice(method: str, uri: str, api_key: str, body=None, application: str = 'rw'):
    """Request to microservice method"""
    try:
        session = Session()
        request_config = Request(
            method=method,
            url=GATEWAY_URL + uri,
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer ' + MICROSERVICE_TOKEN,
                'x-api-key': api_key,
                'APP_KEY': application
            },
        )
        if body:
            request_config.data = json.dumps(body)
        prepped = session.prepare_request(request_config)

        response = session.send(prepped)
    except Exception as error:
        raise error

    try:
        return response.json()
    except Exception:
        raise NotFound(response.text)
