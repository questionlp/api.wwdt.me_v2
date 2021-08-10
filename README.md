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

The [API-CHANGES.md](API-CHANGES.md) document details the changes that were
made from v1.0 to v2.0, including: API response object, API endpoints and API
documentation.

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
