import json
import requests
from flask import request, jsonify, Response
from requests import Session, Request
from werkzeug.datastructures import ImmutableMultiDict

from RWAPIMicroservicePython.errors import NotFound, ApiKeyError, ValidationError

GATEWAY_URL = None
MICROSERVICE_TOKEN = None
REQUIRE_API_KEY = None


def register(app, gateway_url, token, require_api_key):
    @app.after_request
    def set_cors_headers(response):
        response.headers["access-control-allow-origin"] = "*"
        response.headers["access-control-allow-headers"] = "upgrade-insecure-requests"
        response.headers["access-control-allow-credentials"] = "true"
        response.headers["access-control-allow-methods"] = "OPTIONS,GET,PUT,POST,PATCH,DELETE"
        return response

    global MICROSERVICE_TOKEN, GATEWAY_URL, REQUIRE_API_KEY
    MICROSERVICE_TOKEN = token
    GATEWAY_URL = gateway_url
    REQUIRE_API_KEY = require_api_key

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

        inject_request_validation_data(request_validation_data)

        # http_args = request.args.to_dict()
        # http_args['loggedUser'] = logged_user_response.text
        # request.args = ImmutableMultiDict(http_args)

    def inject_request_validation_data(request_validation_data):
        http_args = request.args.to_dict()

        if 'user' in request_validation_data and 'data' in request_validation_data['user']:
            http_args['loggedUser'] = json.dumps(request_validation_data['user']['data'])
        else:
            http_args['loggedUser'] = '{}'
        request.args = ImmutableMultiDict(http_args)

    def get_logger_user():
        if 'x-api-key' not in request.headers and REQUIRE_API_KEY:
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


def request_to_microservice(config):
    """Request to microservice method"""
    try:
        session = Session()
        request_config = Request(
            method=config.get('method'),
            url=GATEWAY_URL + config.get('uri'),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer ' + MICROSERVICE_TOKEN,
                'APP_KEY': config.get('application', 'rw')
            },
        )
        if 'body' in config:
            request_config.data = json.dumps(config.get('body'))
        prepped = session.prepare_request(request_config)

        response = session.send(prepped)
    except Exception as error:
        raise error

    try:
        return response.json()
    except Exception:
        raise NotFound(response.text)
