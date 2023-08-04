USER = {
    "id": "1a10d7c6e0a37126611fd7a5",
    "name": "test user",
    "role": "USER",
    "provider": "local",
    "email": "user@control-tower.org",
    "extraUserData": {
        "apps": [
            "rw",
            "gfw",
            "gfw-climate",
            "prep",
            "aqueduct",
            "forest-atlas",
            "data4sdgs"
        ]
    }
}

MICROSERVICE = {
    "id": "microservice",
    "createdAt": "2022-09-14"
}

APPLICATION = {
    "data": {
        "type": "applications",
        "id": "649c4b204967792f3a4e52c9",
        "attributes": {
            "name": "grouchy-armpit",
            "organization": None,
            "user": None,
            "apiKeyValue": "api-key-test",
            "createdAt": "2023-06-28T15:00:48.149Z",
            "updatedAt": "2023-06-28T15:00:48.149Z"
        }
    }
}


def mock_request_validation(mocker, user=USER, application=APPLICATION['data'], microservice_token='microserviceToken'):
    response_json = {}
    if user is not None:
        response_json['user'] = {'data': user}
    if application is not None:
        response_json['application'] = {'data': application}

    return mocker.post('/v1/request/validate',
                       request_headers={'Authorization': 'Bearer {}'.format(microservice_token)},
                       status_code=200,
                       json=response_json
                       )


def mock_request_validation_invalid_token(mocker, microservice_token='microserviceToken'):
    return mocker.post('/v1/request/validate',
                       request_headers={'Authorization': 'Bearer {}'.format(microservice_token)},
                       status_code=401,
                       json={
                           "errors": [
                               {
                                   "status": 401,
                                   "detail": "Your token is outdated. Please use /auth/login to login and /auth/generate-token to generate a new token."
                               }
                           ]
                       })
