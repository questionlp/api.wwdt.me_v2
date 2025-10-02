# Wait Wait Don't Tell Me! Stats API v2.0

## Overview

The Stats API is written in Python and is built on [FastAPI](https://fastapi.tiangolo.com/) and provides endpoints that can be used to query guest, host, location, panelist, scorekeeper, and show data from a copy of the [Wait Wait Don't Tell Me! Stats database](https://github.com/questionlp/wwdtm_database).

Please note that version 1.0 of the Stats API has now been deprecated.

## Requirements

- Python 3.10 through 3.12. Python 3.13 is currently not validated.
- MySQL Server 8.0 or newer, or another MySQL Server distribution based on MySQL Server 8.0 or newer, hosting a version of the aforementioned Wait Wait Don't Tell Me! Stats database

## Changes from v1.0

Stats API v2.0 not only brings a significant change on web frameworks, migrating from [Flask](https://flask.palletsprojects.com/) to FastAPI, but also breaks compatibility with v1.0 and in terms of API documentation.

For additional details on the breaking changes that the new version brings, refer to the [API-CHANGES.md](API-CHANGES.md) document. The document details the new API response object format, changes in API endpoints, and migrating to OpenAPI-based documentation.

## Known Issues

### OpenAPI 3.0 Specification and Response Models

The application makes significant use of `Optional`, `Union`, and `Tuple` types in the properties for the various response models. This is a necessity due to the way objects are built and returned from [wwdtm](https://github.com/questionlp/wwdtm). Unfortunately, OpenAPI 3.0, the version of the specification that FastAPI supports, does not provide analogs for those types in its specification.

This issue doesn't come up when querying the API through Swagger UI or directly using Postman; but, if you've imported the generated OpenAPI JSON into Postman, then run queries and/or tests, it will result in warnings and/or errors being reported about type mismatches (i.e.: returns `null` instead of a string).

## Installation

Refer to [INSTALLING.md](INSTALLING.md) for information on how to set up an instance of this web application that can be served through [Gunicorn](https://gunicorn.org) and [NGINX](https://nginx.org/).

## Code of Conduct

If you would like contribute to this project, please make sure to review both the [Code of Conduct](./CODE_OF_CONDUCT.md) and the [Contributing](./CONTRIBUTING.md) documents in this repository.

### AI Generated Code

Please note that this project does not accept pull requests or bugfixes that include code that has been partially or wholly generated using AI.

## License

This web application is licensed under the terms of the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
