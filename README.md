# Wait Wait Don't Tell Me! Stats API v2.0

## Overview

The Stats API is written in Python and is built on
[FastAPI](https://fastapi.tiangolo.com/) and provides endpoints that can be
used to query guest, host, location, panelist, scorekeeper, and show data from
a copy of the [Wait Wait Don't Tell Me! Stats database](https://github.com/questionlp/wwdtm_database).

If you're looking for the previous version of the Stats API, check out the
[api.wwdt.me](https://github.com/questionlp/api.wwdt.me) repository on
GitHub.

## Requirements

- Python 3.8 or newer
- MySQL or MariaDB Server hosting a version of the aforementioned Wait Wait
Don't Tell Me! Stats database

## Changes from v1.0

Stats API v2.0 not only brings a significant change on web frameworks,
migrating from [Flask](https://flask.palletsprojects.com/) to FastAPI, but
also breaks compatibility with v1.0 and in terms of API documentation.

For additional details on the breaking changes that the new version brings,
refer to the [API-CHANGES.md](API-CHANGES.md) document. The document details
the new API response object format, changes in API endpoints, and migrating
to OpenAPI-based documentation.

## Known Issues

### OpenAPI 3.0 Specification and Response Models

The application makes significant use of `Optional`, `Union`, and `Tuple`
types in the properties for the various response models. This is a necessity
due to the way objects are built and returned from
[libwwdtm](https://github.com/questionlp/libwwdtm). Unfortunately, OpenAPI 3.0,
the version of the specification that FastAPI supports, does not provide
analogs for those types in its specification.

This issue doesn't come up when querying the API through Swagger UI or directly
using Postman; but, if you've imported the generated OpenAPI JSON into Postman,
then run queries and/or tests, it will result in warnings and/or errors being
reported about type mismatches (i.e.: returns `null` instead of a string).

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
