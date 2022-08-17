# Changes

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
