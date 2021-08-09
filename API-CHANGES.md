# Wait Wait Stats API v2.0 Changes

This document details the API changes between `v1.0` and `v2.0` of the Wait
Wait Don't Tell Me! Stats API. `v2.0` brings changes in both the response
objects and in API endpoint URLs for Guests, Hosts, Locations, Panelists,
Scorekeeper, and Shows.

## Response Object Changes

Response objects returned by `v1.0` of the Stats API followed the
[JSend](https://github.com/omniti-labs/jsend) specification; which, includes
status, data, and/or messages in the JSON response object.

This change was to keep the response object for successful requests as simple
as possible; while, making use of FastAPI's validation and response message
functionality.

With `v2.0`, successful responses will return only the data object requested
for that particular endpoint, along with an HTTP status code of `200`. Any
requests that leads to a validation error will return an object with an
explanation of the validation error, along with an HTTP status
`422 Unprocessable Entity`.

Requests that lead to no data being found will return a response object with a
key/value pair containing a brief message and either an HTTP status code of
`404 Not Found`.

## Endpoint Changes

