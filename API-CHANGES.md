# Wait Wait Stats API v2.0 Changes

This document details the API changes between v1.0 and v2.0 of the Wait Wait
Don't Tell Me! Stats API. v2.0 brings changes in both the response objects and
in API endpoint URLs for Guests, Hosts, Locations, Panelists, Scorekeeper, and
Shows.

## Response Object Changes

Response objects returned by v1.0 of the Stats API followed the
[JSend](https://github.com/omniti-labs/jsend) specification; which, includes
status, data, and/or messages in the JSON response object.

This change was to keep the response object for successful requests as simple
as possible; while, making use of FastAPI's validation and response message
functionality.

With v2.0, successful responses will return only the data object requested for
that particular endpoint, along with an HTTP status code of `200`. Any requests
that leads to a validation error will return an object with an explanation of
the validation error, along with an HTTP status `422 Unprocessable Entity`.

Requests that lead to no data being found will return a response object with a
key/value pair containing a brief message and either an HTTP status code of
`404 Not Found`.

## Endpoint Changes

The following tables list out the changes in API endpoints from v1.0 to v2.0.

### Guests

| v1.0                               | v2.0                               |
|------------------------------------|------------------------------------|
| /v1.0/guests                       | /v2.0/guests                       |
| /v1.0/guests/`id`                  | /v2.0/guests/id/`id`               |
| /v1.0/guests/`id`/details          | /v2.0/guests/details/id/`id`       |
| /v1.0/guests/details               | /v2.0/guests/details               |
| /v1.0/guests/slug/`slug`           | /v2.0/guests/slug/`slug`           |
| /v1.0/guests/slug/`slug`/details   | /v2.0/guests/details/slug/`slug`   |

### Hosts

| v1.0                               | v2.0                               |
|------------------------------------|------------------------------------|
| /v1.0/hosts                        | /v2.0/hosts                        |
| /v1.0/hosts/`id`                   | /v2.0/hosts/id/`id`                |
| /v1.0/hosts/`id`/details           | /v2.0/hosts/details/id/`id`        |
| /v1.0/hosts/details                | /v2.0/hosts/details                |
| /v1.0/hosts/slug/`slug`            | /v2.0/hosts/slug/`slug`            |
| /v1.0/hosts/slug/`slug`/details    | /v2.0/hosts/details/slug/`slug`    |

### Locations

| v1.0                               | v2.0                                   |
|------------------------------------|----------------------------------------|
| /v1.0/locations                    | /v2.0/locations                        |
| /v1.0/locations/`id`               | /v2.0/locations/id/`id`                |
| /v1.0/locations/`id`/recordings    | /v2.0/locations/recordings/id/`id`     |
| /v1.0/locations/recordings         | /v2.0/locations/recordings             |
| *N/A*                              | /v2.0/locations/slug/`slug`            |
| *N/A*                              | /v2.0/locations/recordings/slug/`slug` |

### Panelists

| v1.0                               | v2.0                               |
|------------------------------------|------------------------------------|
| /v1.0/panelists                    | /v2.0/panelists                    |
| /v1.0/panelists/`id`               | /v2.0/panelists/id/`id`            |
| /v1.0/panelists/`id`/details       | /v2.0/panelists/details/id/`id`    |
| /v1.0/panelists/`id`/scores        | /v2.0/panelists/scores/id/`id`     |
| /v1.0/panelists/`id`/scores/ordered-pair | /v2.0/panelists/scores/ordered-pair/id/`id` |
| /v1.0/panelists/details            | /v2.0/panelists/details            |
| /v1.0/panelists/slug/`slug`        | /v2.0/panelists/slug/`slug`        |
| /v1.0/panelists/slug/`slug`/details | /v2.0/panelists/details/slug/`slug` |
| /v1.0/panelists/slug/`slug`/scores | /v2.0/panelists/scores/slug/`slug` |
| /v1.0/panelists/slug/`slug`/ordered-pair | /v2.0/hosts/scores/ordered-pair/slug/`slug` |

### Scorekeepers

| v1.0                               | v2.0                               |
|------------------------------------|------------------------------------|
| /v1.0/scorekeepers                 | /v2.0/scorekeepers                 |
| /v1.0/scorekeepers/`id`            | /v2.0/scorekeepers/id/`id`         |
| /v1.0/scorekeepers/`id`/details    | /v2.0/scorekeepers/details/id/`id` |
| /v1.0/scorekeepers/details         | /v2.0/scorekeepers/details         |
| /v1.0/scorekeepers/slug/`slug`     | /v2.0/scorekeepers/slug/`slug`     |
| /v1.0/scorekeepers/slug/`slug`/details | /v2.0/scorekeepers/details/slug/`slug` |

### Shows

| v1.0                               | v2.0                               |
|------------------------------------|------------------------------------|
| /v1.0/shows                        | /v2.0/shows                        |
| /v1.0/shows/`id`                   | /v2.0/shows/id/`id`                |
| /v1.0/shows/`id`/details           | /v2.0/shows/details/id/`id`        |
| /v1.0/shows/date/`year`            | /v2.0/shows/date/`year`            |
| /v1.0/shows/date/`year`/details    | /v2.0/shows/details/date/`year`    |
| /v1.0/shows/date/`year`/`month`    | /v2.0/shows/date/`year`/`month`    |
| /v1.0/shows/date/`year`/`month`/details | /v2.0/shows/details/date/`year`/`month` |
| /v1.0/shows/date/`year`/`month`/`day` | /v2.0/shows/date/`year`/`month`/`day` |
| /v1.0/shows/date/`year`/`month`/`day`/details | /v2.0/shows/details/date/`year`/`month`/`day` |
| /v1.0/shows/date/iso/`yyyy-mm-dd`  | /v2.0/shows/date/iso/`yyyy-mm-dd`  |
| /v1.0/shows/date/iso/`yyyy-mm-dd`/details | /v2.0/shows/details/iso/`yyyy-mm-dd` |
| *N/A*                              | /v2.0/shows/dates/                 |
| /v1.0/shows/details                | /v2.0/shows/details                |
| /v1.0/shows/recent                 | /v2.0/shows/recent                 |
| /v1.0/shows/recent/details         | /v2.0/shows/details/recent         |

## Documentation Changes

Documentation for v1.0 of the API was handled as an external project based on
the dormant [Docbox](https://github.com/tmcw/docbox) documentation system.

With v2.0 being built on FastAPI, which is based on [OpenAPI](https://www.openapis.org/),
the framework can be set up to present API documentation through
[Swagger UI](https://swagger.io/tools/swagger-ui/) and/or
[Redoc](https://github.com/Redocly/redoc). To facilitate that, v2.0 makes
significant use of Pydantic to build out the objects and includes much of the
documentation while declaring routes and within Python docstrings.
