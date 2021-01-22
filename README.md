# RW API microservice utility for Python+Flask applications

[![Build Status](https://travis-ci.com/resource-watch/rw-api-microservice-python.svg?branch=main)](https://travis-ci.com/resource-watch/rw-api-microservice-python)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fe857a0082ab7d0bbd64/test_coverage)](https://codeclimate.com/github/resource-watch/rw-api-microservice-python/test_coverage)

Library to register and integrate microservices in the [RW API](https://api.resourcewatch.org/).


## Requirements

This library is tested to work with following Python versions:
- 3.6+
- 2.7 (legacy)

Additionally, it requires the following Python libraries: 
- Flask (tested with v1.1.1)
- Requests

## Install

```shell
pip install RWAPIMicroservicePython
```

## Use in microservice




## Configuration

, mode, ct_url=False, url=False, active=True, delay=5.0

These are the values you'll need to provide when using this library:

- app: the [Flask](https://flask.palletsprojects.com) `app`.
- info: (**deprecated**) Object containing the microservice details. See [this link](https://github.com/resource-watch/dataset/blob/ab23e379362680e9899ac8f191589988f0b7c1cd/app/microservice/register.json) for an example.
- swagger: (**deprecated**) Object, in Swagger format, of the endpoints offered by the microservice to API end users.
- name: the name of the service.
- mode: (**deprecated**)  if set to `RWAPIMicroservicePython.AUTOREGISTER_MODE`, the library will register the microservice on Control Tower when initialized. This option will be removed soon.
- ct_url: the URL of the API as a whole, where all other services will be reachable.
- url: the URL where your service will be reachable
- token: JWT token to use on calls to other services.
- api_version: (optional) string representing the api version of the endpoints called when using `request_to_microservice`. Typically, it should have `v1` as value.

