# RW API microservice utility for Python+Flask applications

[![Build Status](https://travis-ci.com/resource-watch/rw-api-microservice-python.svg?branch=main)](https://travis-ci.com/resource-watch/rw-api-microservice-python)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fe857a0082ab7d0bbd64/test_coverage)](https://codeclimate.com/github/resource-watch/rw-api-microservice-python/test_coverage)

Library to register and integrate microservices in the [RW API](https://api.resourcewatch.org/).


## Requirements


## Install


## Use in microservice




## Configuration

These are the values you'll need to provide when using this library:

- info: (**deprecated**) Object containing the microservice details. See [this link](https://github.com/resource-watch/dataset/blob/ab23e379362680e9899ac8f191589988f0b7c1cd/app/microservice/register.json) for an example.
- swagger: (**deprecated**) Object, in Swagger format, of the endpoints offered by the microservice to API end users.
- name: the name of the service.
- baseURL: the URL of the API as a whole, where all other services will be reachable.
- url: the URL where your service will be reachable
- token: JWT token to use on calls to other services.
