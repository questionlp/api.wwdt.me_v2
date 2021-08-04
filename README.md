# Wait Wait Don't Tell Me! Stats API v2.0

## Overview

API service, written in Python and build on [FastAPI](https://fastapi.tiangolo.com/),
that provides endpoints to query guest, host, location, panelist, scorekeeper
and show data from the [Wait Wait Don't Tell Me! Stats database](https://github.com/questionlp/wwdtm_database).

## Requirements

- Python 3.8 or newer
- MySQL or MariaDB database containing data from the Wait Wait... Don't Tell
  Me! Stats Page database

## Changes from v1.0

The new v2.0 brings not only a significant change on web frameworks, from
[Flask](https://flask.palletsprojects.com/) to FastAPI, but also breaks
compatibility with v1.0 and in terms of API documentation.

### API Routes

To signify the change in API version, all endpoints for v2.0 will be served
with a route prefix of `v2.0` instead of `v1.0`. v1.0 will still be made
available for some time and will be served using the existing Flask-based
codebase.

An effort was made to keep the remaining portions of the endpoints the same
across both versions. This allows for easier migration from v1.0 to v2.0
by only changing one part of the request URL.

### Breaking Backwards Compatibility
The new version moves away from using [JSend](https://github.com/omniti-labs/jsend)
specification for JSON response format. The change was made to keep the
response data simple and leverage FastAPI's validation and response handling.

As such, queries against corresponding endpoints will return JSON that does not
have the JSend response wrapper. Successful requests to v1.0 returns data
within the `data` property of the returned object. In v2.0, the data is
returned unencapsulated and directly to the user agent.

### Documentation Changes

Documentation for v1.0 of the API was handled as an external project based on
the dormant [Docbox](https://github.com/tmcw/docbox) documentation system.

With v2.0 being built on FastAPI, which is based on [OpenAPI](https://www.openapis.org/),
the framework can be set up to present API documentation through
[Swagger UI](https://swagger.io/tools/swagger-ui/) and/or
[Redoc](https://github.com/Redocly/redoc). To facilitate that, v2.0 makes
significant use of Pydantic to build out the objects and includes much of the
documentation while declaring routes and within Python docstrings.

## Installation

Refer to [INSTALLING.md](INSTALLING.md) for information on how to set up an
instance of this web application that can be served through
[Gunicorn](https://gunicorn.org) and [NGINX](https://nginx.org/).

## Code of Conduct

This projects follows version 2.1 of the
[Contributor Convenant's](https://www.contributor-covenant.org/) Code of
Conduct. A copy of the [Code of Conduct](CODE_OF_CONDUCT.md) document is
included in this repository.

## License

This library is licensed under the terms of the
[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
