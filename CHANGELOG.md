# 3.0.0-rc.2

- Improve typing definition

# 3.0.0-rc.1

- Add `/healthcheck` endpoint
- Improve documentation

# 3.0.0-beta.6

- Support `request_to_microservice` calls without api key for microservices

# 3.0.0-beta.5

- Improve `test_utils` utility methods for testing

# 3.0.0-beta.4

- Add `test_utils` utility methods for testing

# 3.0.0-beta.3

- Add missing boto3 dependency
- Export test mock method

# 3.0.0-beta.2

- Update required dependencies

# 3.0.0-beta.1

- Refactor `request_to_microservice` argument signature
- Add `x-api-key` header to `request_to_microservice`
- Add AWS Cloudwatch logging integration

# 3.0.0-alpha.1

- Bump minimum supported Python version to 3.10
- Update dependencies
- Replace user data loading endpoint with request validation endpoint

# 2.0.0

- Bump minimum supported Python version to 3.7
- Add Python 3.10 and 3.11 support
- Update dependencies

# 1.0.0

- Remove Control Tower support
- `request_to_microservice` no longer prefixes request uris with `/v1`
- Remove `/info` and `/ping` endpoints

# 0.4.0

- Add CORS headers

# 0.3.0

- Pin dependency versions to python 2.7 compatible versions
- Fix issue where `request_to_microservice` would always have a body.

# 0.2.0

- Add error handling for 4xx and 5xx when loading user data.

# 0.1.0

- Initial release