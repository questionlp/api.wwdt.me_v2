# Changes

## 2.10.0.post2

### Component Changes

- Upgrade requests from 2.32.0 to 2.32.3

## 2.10.0.post1

### Component Changes

- Upgrade requests from 2.31.0 to 2.32.0

## 2.10.0

### Application Changes

- Starting with application version 2.10.0 of the Stats API, the minimum required version of the Wait Wait Stats Database is 4.7
- Change the `pronouns` property for Hosts, Panelists and Scorekeepers from returning a string to a list of pronouns
- Add `Pronouns` and `PronounsInfoList` models
- Add new Pronouns endpoints to retrieve all available pronouns or individual pronouns values

## 2.9.1.post1

**Note:** The `APP_VERSION` was not correctly incremented with version 2.9.1 and has been corrected with this release.

### Component Changes

- Upgrade Jinja2 from 3.1.3 to 3.1.4

## 2.9.1

### Application Changes

- Create `LocationCoordinates` and `ShowLocationCoordinates` models to contain location latitude and longitude values for locations and shows respectively

### Component Changes

- Upgrade wwdtm from 2.9.0 to 2.9.1

## 2.9.0 (Unreleased)

### Application Changes

- Starting with application version 2.9.0 of the Stats API, the minimum required version of the Wait Wait Stats Database is 4.6
- Add `latitude` and `longitude` to any location object returned. If a value for either are present in the Stats Database, a string representation of a decimal would be returned. If not, `null` would be returned.
- Add `pronouns` to any host, panelist and scorekeeper object returned. If a corresponding value is present in the State Database, a string would be returned. If not, `null` would be returned.

### Component Changes

- Upgrade wwdtm from 2.8.1 to 2.9.0
- Upgrade fastapi from 0.109.1 to 0.110.2
- Upgrade pydantic from 2.5.3 to 2.7.0

## 2.8.6

### Component Changes

- Upgrade gunicorn from 21.2.0 to 22.0.0

### Development Changes

- Upgrade ruff from 0.1.13 to 0.3.6
- Upgrade pytest from 7.4.4 to 8.1.1

## 2.8.5

### Development Changes

- Upgrade black from 23.12.1 to 24.3.0

## 2.8.4

### Component Changes

- Upgrade wwdtm from 2.8.0 to 2.8.1, which includes fixing an issue of panelists not being sorted by their decimal scores properly

## 2.8.3

### Component Changes

- Upgrade fastapi from 0.109.0 to 0.109.1

## 2.8.2

### Application Changes

- Add support for GitHub sponsorship link in the side pop-out nav, dropdown nav menu and in the footer by way of the `settings.github_sponsor_url` config key

## 2.8.1

### Application Changes

- Update Show route docstrings to include mention of NPR.org show URL in the returned data
- Add support for Patreon link in the side pop-out nav, dropdown nav menu and in the footer by way of the `settings.patreon_url` config key

## 2.8.0

### Application Changes

- Starting with application version 2.8.0 of the Stats API, the minimum required version of the Wait Wait Stats Database is 4.5
- Add support for returning show URL value from the Wait Wait Stats Database as `show_url` in returned show objects
- Code cleanup and updating docstrings

### Component Changes

- Upgrade wwdtm from 2.6.1 to 2.8.0
- Upgrade pydantic from 2.5.2 to 2.5.3
- Upgrade fastapi from 0.104.1 to 0.109.0
- Upgrade uvicorn from 0.24.0.post1 to 0.26.0
- Upgrade httpx from 0.25.2 to 0.26.0

### Development Changes

- Switch to Ruff for code linting and formatting (with the help of Black)
- Upgrade black from 23.11.0 to 23.12.1
- Upgrade pytest from 7.4.3 from 7.4.4

## 2.7.2

### Component Changes

- Upgrade jinja2 from 3.1.2 to 3.1.3

## 2.7.1

### Component Changes

- Upgrade wwdtm from 2.6.0 to 2.6.1

## 2.7.0

### Application Changes

- Add support for shows that have multiple Bluff the Listener-like segments.
- This changes includes renaming the `bluff` key returned in show details objects to `bluffs`. The new `bluffs` key now returns an array of objects that includes a `segment` key used to denote which segment it is referencing, along with the `chosen_panelist` and `correct_panelist` objects.

### Component Changes

- Upgrade wwdtm from 2.5.0 to 2.6.0, which requires Wait Wait Stats Database version 4.4 or higher

## 2.6.0

**Starting with version 2.6.0, support for all versions of Python prior to 3.10 have been deprecated.**

### Component Changes

- Upgrade wwdtm from 2.4.1 to 2.5.0, which drops supports for Python versions prior to 3.10 and includes:
  - Upgrade MySQL Connector/Python from 8.0.33 to 8.2.0
  - Upgrade numpy from 1.24.4 to 1.26.0
- Upgrade pydantic from 2.3.0 to 2.5.2
- Upgrade fastapi from 0.103.1 to 0.104.1
- Upgrade uvicorn from 0.23.2 to 0.24.0.post1
- Upgrade httpx from 0.24.1 to 0.25.2
- Upgrade email-validator from 2.0.0.post2 to 2.1.0.post1

### Development Changes

- Upgrade pytest from 7.4.0 to 7.4.3
- Upgrade black from 23.7.0 to 23.11.0
- Remove `py38` and `py39` from `tool.black` in `pyproject.toml`
- Bump minimum pytest version from 7.0 to 7.4 in `pyproject.toml`

## 2.5.0

### Application Changes

- Migrate to Pydantic 2, which requires re-working of models, which includes:
  - Using [bump-pydantic](https://github.com/pydantic/bump-pydantic) to migrate to Pydantic 2
  - Replacing `conint` and `constr` with `Annotated[int, Path()]` and `Annotated[str, Path()]` respectively in routes
  - Replacing `strip_whitespace=True` to `string.strip()` when passing in values to a method
- Adding titles via `Path(title=)` to path elements in routes where applicable
- Correct spelling errors

### Component Changes

- Upgrade pydantic from `<2` to 2.3.0
- Upgrade wwdtm from 2.4.0 to 2.4.1, which includes:
  - Upgrading numpy from 1.24.3 to 1.24.4
  - Upgrading pytz from 2023.3 to 2023.3.post1

## 2.4.1

### Application Changes

- Correct typo in the docstring for `LocationRecordings` model

### Component Changes

- Upgrade wwdtm from 2.3.0 to 2.4.0

## 2.4.0

### Application Changes

- Add support for Panelist Lightning Start and Correct decimal fields for the appropriate models
- Panelist Lightning Start and Correct decimal values will be added as additional fields rather than replacing the current fields

### Component Changes

- Upgrade wwdtm from 2.2.0 to 2.3.0

## 2.3.2

### Application Changes

- Fix issue where `panelists/scores/id` and `panelists/scores/slug` return scores as `int` instead of `Decimal` due to `Union[int, Decimal]` would return an `int`. Switched to `Union[Decimal, int]` to allow `Decimal` to take precedence

## 2.3.1

### Component Changes

- Change pydantic version pin from "==1.10.12" to "<2" to include potential future updates to 1.x while blocking 2.x or higher

## 2.3.0

### Application Changes

- Add support for new column in the Wait Wait Stats Database that stores panelist scores as a decimal
- Add a new settings configuration key, `use_decimal_scores`, to enable or disable the new feature

### Component Changes

- Upgrade wwdtm from 2.1.0 to 2.2.0
- Upgrade fastapi from 0.101.0 to 0.103.0
- Pin pydantic to 1.10.12
  - FastAPI breaks with Pydantic version >=2.0.0

## 2.2.0

### Component Changes

- Upgrade fastpi from 0.98.0 to 0.101.0
- Upgrade uvicorn from 0.22.0 to 0.23.2
- Upgrade gunicorn from 20.1.0 to 21.2.0
- Upgrade aiofiles from 23.1.0 to 23.2.1
- Upgrade email-validator from 1.3.1 to 2.0.0.post2

### Development Changes

- Upgrade flake8 from 6.0.0 to 6.1.0
- Upgrade pycodestyle from 2.10.0 to 2.11.0
- Upgrade pytest from 7.3.1 to 7.4.0
- Upgrade black from 23.3.0 to 23.7.0

## 2.1.4

### Component Changes

- Upgrade wwdtm from 2.0.9 to 2.1.0
- Upgrade fastapi from 0.95.1 to 0.98.0
- Upgrade uvicorn from 0.21.0 to 0.22.0
- Upgrade httpx from 0.24.0 to 0.24.1
- Upgrade requests from 2.28.2 to 2.31.0

## 2.1.3

### Component Changes

- Upgrade wwdtm from 2.0.8 to 2.0.9, which also includes the following changes:
  - Upgrade MySQL Connector/Python from 8.0.31 to 8.0.33
  - Upgrade NumPy from 1.23.4 to 1.24.2
  - Upgrade python-slugify from 6.1.2 to 8.0.1
  - Upgrade pytz from 2022.6 to 2023.3
- Upgrade fastapi from 0.88.0 to 0.95.1
- Upgrade httpx from 0.23.1 to 0.24.0
- Upgrade uvicorn from 0.20.0 to 0.21.1
- Upgrade aiofiles from 22.1.0 to 23.1.0
- Upgrade email-validator from 1.3.0 to 1.3.1
- Upgrade requests from 2.28.1 to 2.28.2

### Development Changes

- Move pytest configuration from `pytest.ini` into `pyproject.toml`
- Upgrade flake8 from 5.0.4 to 6.0.0
- Upgrade pycodestyle from 2.9.1 to 2.10.0
- Upgrade pytest from 7.2.0 to 7.3.1
- Upgrade black from 22.10.0 to 23.3.0

## 2.1.2

### Application Changes

- Add `/v1.0` and `/v1.0/docs` routes that redirect back to `/` as part of deprecating Stats API v1.0
- Remove links to Stats API v1.0 docs and update v1.0 deprecation message

## 2.1.1

### Application Changes

- Better handling of how `app.metadata.app_metadata` is populated in case the corresponding values are not set in `config.json`
- Add validation of `contact_email`, `contact_name` and `contact_url` values when populating `app.metadata.app_metadata`

## 2.1.0

### Application Changes

- Added `settings` section to the application `config.json` and `config.json.dist` template file with the following keys:
  - `stats_url` to set the URL for the Wait Wait Stats Page
  - `contact_email` to set a contact e-mail address for the OpenAPI metadata
  - `contact_name` to set a contact name for the OpenAPI metadata
  - `contact_url` to set a contact URL for the OpenAPI metadata
- Renamed `load_database_config` in `app.config` to `load_config` that returns a dictionary with `database` and `settings` as keys containing the corresponding values as a dictionary from `config.json`
- Update all references to `app.config.load_database_config` to `app.config.load_config`
- Update `app/metadata.py` to make use of the new contact e-mail, name and URL configuration keys
- Update the `index.html` template to make use of the `stats_url` configuration key

### Component Changes

- Upgrade wwdtm from 2.0.7 to 2.0.8, which also includes the following changes:
  - Upgrade MySQL Connector/Python from 8.0.30 to 8.0.31
  - Upgrade NumPy from 1.23.2 to 1.23.4
  - Upgrade python-slugify from 5.0.2 to 6.1.2
  - Upgrade pytz from 2022.2.1 to 2022.6
- Upgrade fastapi from 0.85.0 to 0.88.0
  - Add httpx 0.23.1 as a requirement for fastapi 0.88.0
- Upgrade uvicorn from 0.18.3 to 0.20.0
- Upgrade aiofiles from 0.8.0 to 22.1.0
- Upgrade email-validator from 1.2.1 to 1.3.0

### Development Changes

- Upgrade flake8 from 4.0.1 to 5.0.4
- Upgrade pycodestyle from 2.8.0 to 2.9.1
- Upgrade pytest from 7.1.2 to 7.2.0
- Upgrade black from 22.6.0 to 22.10.0

## 2.0.6

### Application Changes

- Explicitly return `text/plain` as the media type for `/robots.txt`

### Component Changes

- Upgrade fastapi from 0.79.0 to 0.85.0
- Upgrade uvicorn from 0.18.2 to 0.18.3
- Upgrade aiofiles from 0.8.0 to 22.1.0

### Development Changes

- Upgrade pytest from 7.1.2 to 7.1.3

## 2.0.5

### Application Changes

- Officially deprecate Stats API v1.0 and add a notice on the main index page. No other application changes were made.

## 2.0.4

### Component Changes

- Upgrade wwdtm from 2.0.5 to 2.0.7, which also includes the following changes:
  - Upgrade MySQL Connector/Python from 8.0.28 to 8.0.30
  - Upgrade NumPy from 1.22.3 to 1.23.2
  - Upgrade pytz from 2022.1 to 2022.2.1
- Upgrade requests from 2.27.1 to 2.28.1

### Development Changes

- Correct required version of Black from 22.3.0 to 22.6.0 in `requirements-dev.txt`

## 2.0.3

### Component Changes

- Upgrade fastapi from 0.78.0 to 0.79.0
- Upgrade uvicorn from 0.17.6 to 0.18.2

### Development Changes

- Upgrade black from 22.3.0 to 22.6.0
- Change Black `target-version` to remove `py36` and `py37`, and add `py310`

## 2.0.2

### Component Changes

- Upgrade fastapi from 0.75.1 to 0.78.0
- Upgrade jinja2 from 3.1.1 to 3.1.2
- Upgrade email-validator from 1.1.3 to 1.2.1

### Development Changes

- Upgrade pytest from 6.2.5 to 7.1.2
- Upgrade black from 22.1.0 to 22.3.0

## 2.0.1

### Component Changes

- Upgrade fastapi from 0.73.0 to 0.75.1
- Upgrade uvicorn from 0.17.4 to 0.17.6
- Upgrade jinja2 from 3.0.3 to 3.1.1

## 2.0.0

- Brand new development for Wait Wait Stats API built on [FastAPI](http://fastapi.tiangolo.com) and version 2 of [wwdtm](https://github.com/questionlp/wwdtm)

## Pre-Release Versions

For a list of changes for pre-release versions of the Wait Wait Stats API, check out the [Releases](https://github.com/questionlp/api.wwdt.me_v2/releases) page for [api.wwdt.me_v2](https://github.com/questionlp/api.wwdt.me_v2) on GitHub.
