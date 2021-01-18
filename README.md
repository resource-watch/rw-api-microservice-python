# RW API microservice utility for Python+Flask applications


Library to register and integrate microservices in the [RW API](https://api.resourcewatch.org/).


## Requirements


## Install


## Use in microservice




## Configuration

These are the values you'll need to provide when using this library:

- info: (**deprecated**) Object containing the microservice details. See [this link](https://github.com/resource-watch/dataset/blob/ab23e379362680e9899ac8f191589988f0b7c1cd/app/microservice/register.json) for an example.
- swagger: (**deprecated**) Object, in Swagger format, of the endpoints offered by the microservice to API end users.
- logger: a `bunyan` logger object, for logging purposes.
- name: the name of the service.
- baseURL: the URL of the API as a whole, where all other services will be reachable.
- url: the URL where your service will be reachable
- token: JWT token to use on calls to other services.
- skipGetLoggedUser: if set to `true`, the library will not intercept `authorization` headers nor fetch and inject the associated user data. This is a temporary functionality, and will be removed soon.
- fastlyEnabled: if set to `true`, the [Fastly](https://www.fastly.com/) integration will be enabled.
- fastlyServiceId and fastlyAPIKey: data for the Fastly integration. See [this link](https://docs.fastly.com/en/guides/finding-and-managing-your-account-info) for details on how to get these values. These values are required if `fastlyEnabled` is `true`.
