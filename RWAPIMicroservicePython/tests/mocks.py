from RWAPIMicroservicePython.tests.constants import USER, APPLICATION


def mock_request_validation(mocker, user=USER, application=APPLICATION['data']):
    response_json = {}
    if user is not None:
        response_json['user'] = {'data': user}
    if application is not None:
        response_json['application'] = {'data': application}

    return mocker.post('http://gateway-url.com/v1/request/validate',
                       request_headers={'Authorization': 'Bearer microserviceToken'},
                       status_code=200,
                       json=response_json
                       )


def mock_request_validation_invalid_token(mocker):
    return mocker.post('http://gateway-url.com/v1/request/validate',
                       request_headers={'Authorization': 'Bearer microserviceToken'},
                       status_code=401,
                       json={
                           "errors": [
                               {
                                   "status": 401,
                                   "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."
                               }
                           ]
                       })
