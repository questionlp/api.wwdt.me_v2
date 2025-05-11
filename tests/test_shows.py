# Copyright (c) 2018-2025 Linh Pham
# api.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing /v2.0/shows routes."""

import pytest
from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app

client = TestClient(app)


def test_get_shows():
    """Test /v2.0/shows route."""
    response = client.get(f"/v{API_VERSION}/shows")
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]


@pytest.mark.parametrize("inclusive", [True, False])
def test_get_shows_best_ofs(inclusive: bool):
    """Test /v2.0/shows/best-ofs route."""
    response = client.get(
        f"/v{API_VERSION}/shows/best-ofs", params={"inclusive": inclusive}
    )
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert shows["shows"][0]["best_of"] is True
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]


@pytest.mark.parametrize("show_id", [1083])
def test_get_show_by_id(show_id: int):
    """Test /v2.0/shows/id/{show_id} route."""
    response = client.get(f"/v{API_VERSION}/shows/id/{show_id}")
    show = response.json()

    assert response.status_code == 200
    assert "id" in show
    assert show["id"] == show_id
    assert "date" in show
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show


@pytest.mark.parametrize("show_id", [0])
def test_get_show_by_id_not_found(show_id: int):
    """Test /v2.0/shows/id/{show_id} route."""
    response = client.get(f"/v{API_VERSION}/shows/id/{show_id}")
    show = response.json()

    assert response.status_code == 404
    assert "detail" in show


@pytest.mark.parametrize("show_date", ["2018-10-27"])
def test_get_show_by_date_string(show_date: str):
    """Test /v2.0/shows/date/iso/{show_id} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/iso/{show_date}")
    show = response.json()

    assert response.status_code == 200
    assert "id" in show
    assert "date" in show
    assert show["date"] == show_date
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show


@pytest.mark.parametrize("show_date", ["1970-01-01"])
def test_get_show_by_date_string_not_found(show_date: str):
    """Test /v2.0/shows/date/iso/{show_id} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/iso/{show_date}")
    show = response.json()

    assert response.status_code == 404
    assert "detail" in show


@pytest.mark.parametrize("year", [2006])
def test_get_shows_by_year(year: int):
    """Test /v2.0/shows/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}")
    shows = response.json()
    formatted_year = f"{year:04}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]


@pytest.mark.parametrize("year", [9999])
def test_get_shows_by_year_not_found(year: int):
    """Test /v2.0/shows/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year", [2006])
def test_get_shows_by_year_best_ofs(year: int):
    """Test /v2.0/shows/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/best-ofs")
    shows = response.json()
    formatted_year = f"{year:04}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]


@pytest.mark.parametrize("year", [9999])
def test_get_shows_by_year_best_ofs_not_found(year: int):
    """Test /v2.0/shows/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/best-ofs")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year", [2006])
def test_get_shows_by_year_repeat_best_ofs(year: int):
    """Test /v2.0/shows/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/repeat-best-ofs")
    shows = response.json()
    formatted_year = f"{year:04}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]


@pytest.mark.parametrize("year", [9999])
def test_get_shows_by_year_repeat_best_ofs_not_found(year: int):
    """Test /v2.0/shows/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/repeat-best-ofs")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year", [2006])
def test_get_shows_by_year_repeats(year: int):
    """Test /v2.0/shows/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/repeats")
    shows = response.json()
    formatted_year = f"{year:04}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]


@pytest.mark.parametrize("year", [9999])
def test_get_shows_by_year_repeats_not_found(year: int):
    """Test /v2.0/shows/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/repeats")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year, month", [(2006, 6)])
def test_get_shows_by_year_month(year: int, month: int):
    """Test /v2.0/shows/date/{year}/{month} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/{month}")
    shows = response.json()
    formatted_year_month = f"{year:04}-{month:02}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year_month)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]


@pytest.mark.parametrize("year, month", [(9999, 1)])
def test_get_shows_by_year_month_not_found(year: int, month: int):
    """Test /v2.0/shows/date/{year}/{month} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/{month}")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("month, day", [(10, 27)])
def test_get_shows_by_month_day(month: int, day: int):
    """Test /v2.0/shows/date/month-day/{month}/{day} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/month-day/{month}/{day}")
    shows = response.json()
    formatted_month_day = f"{month:02}-{day:02}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].find(formatted_month_day)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]


@pytest.mark.parametrize("month, day", [(2, 30)])
def test_get_shows_by_month_day_not_found(month: int, day: int):
    """Test /v2.0/shows/date/month-day/{month}/{day} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/month-day/{month}/{day}")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year, month, day", [(2018, 10, 27)])
def test_get_show_by_date(year: int, month: int, day: int):
    """Test /v2.0/shows/date/{year}/{month}/{day} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/{month}/{day}")
    show = response.json()
    formatted_date = f"{year:04}-{month:02}-{day:02}"

    assert response.status_code == 200
    assert "id" in show
    assert "date" in show
    assert show["date"] == formatted_date
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show


@pytest.mark.parametrize("year, month, day", [(1998, 2, 30)])
def test_get_show_by_date_not_found(year: int, month: int, day: int):
    """Test /v2.0/shows/date/{year}/{month}/{day} route."""
    response = client.get(f"/v{API_VERSION}/shows/date/{year}/{month}/{day}")
    show = response.json()

    assert response.status_code == 404
    assert "detail" in show


def test_get_all_show_dates():
    """Test /v2.0/shows/dates route."""
    response = client.get(f"/v{API_VERSION}/shows/dates")
    dates = response.json()

    assert response.status_code == 200
    assert "shows" in dates
    assert dates["shows"]


def test_get_shows_details():
    """Test /v2.0/shows/details route."""
    response = client.get(f"/v{API_VERSION}/shows/details")
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("inclusive", [True, False])
def test_get_shows_details_best_ofs(inclusive: bool):
    """Test /v2.0/shows/details/best-ofs route."""
    response = client.get(
        f"/v{API_VERSION}/shows/details/best-ofs", params={"inclusive": inclusive}
    )
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert shows["shows"][0]["best_of"] is True
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("show_id", [1083])
def test_get_show_details_by_id(show_id: int):
    """Test /v2.0/shows/details/id/{show_id} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/id/{show_id}")
    show = response.json()

    assert response.status_code == 200
    assert "id" in show
    assert show["id"] == show_id
    assert "date" in show
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show
    assert "location" in show
    assert "description" in show
    assert "host" in show
    assert "scorekeeper" in show
    assert "panelists" in show
    assert "guests" in show


@pytest.mark.parametrize("show_id", [0])
def test_get_show_details_by_id_not_found(show_id: int):
    """Test /v2.0/shows/details/id/{show_id} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/id/{show_id}")
    show = response.json()

    assert response.status_code == 404
    assert "detail" in show


@pytest.mark.parametrize("show_date", ["2018-10-27"])
def test_get_show_details_by_date_string(show_date: str):
    """Test /v2.0/shows/details/date/iso/{show_date} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/iso/{show_date}")
    show = response.json()

    assert response.status_code == 200
    assert "id" in show
    assert "date" in show
    assert show["date"] == show_date
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show
    assert "location" in show
    assert "description" in show
    assert "host" in show
    assert "scorekeeper" in show
    assert "panelists" in show
    assert "guests" in show


@pytest.mark.parametrize("show_date", ["1970-01-01"])
def test_get_show_details_by_date_string_not_found(show_date: str):
    """Test /v2.0/shows/details/date/iso/{show_date} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/iso/{show_date}")
    show = response.json()

    assert response.status_code == 404
    assert "detail" in show


@pytest.mark.parametrize("year", [2006])
def test_get_shows_details_by_year(year: int):
    """Test /v2.0/shows/details/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}")
    shows = response.json()
    formatted_year = f"{year:04}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("year", [9999])
def test_get_shows_details_by_year_not_found(year: int):
    """Test /v2.0/shows/details/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year", [2006])
def test_get_shows_details_by_year_best_ofs(year: int):
    """Test /v2.0/shows/details/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/best-ofs")
    shows = response.json()
    formatted_year = f"{year:04}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("year", [9999])
def test_get_shows_details_by_year_best_ofs_not_found(year: int):
    """Test /v2.0/shows/details/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/best-ofs")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year", [2006])
def test_get_shows_details_by_year_repeat_best_ofs(year: int):
    """Test /v2.0/shows/details/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/repeat-best-ofs")
    shows = response.json()
    formatted_year = f"{year:04}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("year", [9999])
def test_get_shows_details_by_year_repeat_best_ofs_not_found(year: int):
    """Test /v2.0/shows/details/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/repeat-best-ofs")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year", [2006])
def test_get_shows_details_by_year_repeats(year: int):
    """Test /v2.0/shows/details/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/repeats")
    shows = response.json()
    formatted_year = f"{year:04}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("year", [9999])
def test_get_shows_details_by_year_repeats_not_found(year: int):
    """Test /v2.0/shows/details/date/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/repeats")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year, month", [(2006, 6)])
def test_get_shows_details_by_year_month(year: int, month: int):
    """Test /v2.0/shows/details/date/{year}/{month} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/{month}")
    shows = response.json()
    formatted_year_month = f"{year:04}-{month:02}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].startswith(formatted_year_month)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("year, month", [(9999, 1)])
def test_get_shows_details_by_year_month_not_found(year: int, month: int):
    """Test /v2.0/shows/details/date/{year}/{month} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/{month}")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("month, day", [(10, 27)])
def test_get_shows_details_by_month_day(month: int, day: int):
    """Test /v2.0/shows/details/date/month-day/{month}/{day} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/month-day/{month}/{day}")
    shows = response.json()
    formatted_month_day = f"{month:02}-{day:02}"

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert shows["shows"][0]["date"].find(formatted_month_day)
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("month, day", [(2, 30)])
def test_get_shows_details_by_month_day_not_found(month: int, day: int):
    """Test /v2.0/shows/details/date/month-day/{month}/{day} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/month-day/{month}/{day}")
    shows = response.json()

    assert response.status_code == 404
    assert "detail" in shows


@pytest.mark.parametrize("year, month, day", [(2018, 10, 27)])
def test_get_shows_details_by_date(year: int, month: int, day: int):
    """Test /v2.0/shows/details/date/{year}/{month}/{day} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/{month}/{day}")
    show = response.json()
    formatted_date = f"{year:04}-{month:02}-{day:02}"

    assert response.status_code == 200
    assert "id" in show
    assert "date" in show
    assert show["date"] == formatted_date
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show
    assert "location" in show
    assert "description" in show
    assert "host" in show
    assert "scorekeeper" in show
    assert "panelists" in show
    assert "guests" in show


@pytest.mark.parametrize("year, month, day", [(1998, 2, 30)])
def test_get_shows_details_by_date_not_found(year: int, month: int, day: int):
    """Test /v2.0/shows/details/date/{year}/{month}/{day} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/date/{year}/{month}/{day}")
    show = response.json()

    assert response.status_code == 404
    assert "detail" in show


def test_get_random_show_details():
    """Test /v2.0/shows/details/random route."""
    response = client.get(f"/v{API_VERSION}/shows/details/random")
    show = response.json()

    assert response.status_code == 200
    assert "id" in show
    assert "date" in show
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show
    assert "location" in show
    assert "description" in show
    assert "host" in show
    assert "scorekeeper" in show
    assert "panelists" in show
    assert "guests" in show


@pytest.mark.parametrize("year", [1998, 2020])
def test_get_random_show_by_year_details(year: int):
    """Test /v2.0/shows/details/random/year/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/random/year/{year}")
    show = response.json()

    assert response.status_code == 200
    assert "id" in show
    assert "date" in show
    assert str(year) in show["date"]
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show
    assert "location" in show
    assert "description" in show
    assert "host" in show
    assert "scorekeeper" in show
    assert "panelists" in show
    assert "guests" in show


@pytest.mark.parametrize("year", [9999])
def test_get_random_show_by_year_details_not_found(year: int):
    """Test /v2.0/shows/details/random/year/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/details/random/year/{year}")
    show = response.json()

    assert response.status_code == 404
    assert "detail" in show


def test_get_shows_recent_details():
    """Test /v2.0/shows/details/recent route."""
    response = client.get(f"/v{API_VERSION}/shows/details/recent")
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


def test_get_shows_details_repeat_best_ofs():
    """Test /v2.0/shows/details/repeat-best-ofs route."""
    response = client.get(f"/v{API_VERSION}/shows/details/repeat-best-ofs")
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert shows["shows"][0]["best_of"] is True
    assert "repeat_show" in shows["shows"][0]
    assert shows["shows"][0]["repeat_show"] is True
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert isinstance(shows["shows"][0]["original_show_id"], int)
    assert "original_show_date" in shows["shows"][0]
    assert isinstance(shows["shows"][0]["original_show_date"], str)
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


@pytest.mark.parametrize("inclusive", [True, False])
def test_get_shows_details_repeats(inclusive: bool):
    """Test /v2.0/shows/repeats route."""
    response = client.get(
        f"/v{API_VERSION}/shows/details/repeats", params={"inclusive": inclusive}
    )
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert shows["shows"][0]["repeat_show"] is True
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert isinstance(shows["shows"][0]["original_show_id"], int)
    assert "original_show_date" in shows["shows"][0]
    assert isinstance(shows["shows"][0]["original_show_date"], str)
    assert "location" in shows["shows"][0]
    assert "description" in shows["shows"][0]
    assert "host" in shows["shows"][0]
    assert "scorekeeper" in shows["shows"][0]
    assert "panelists" in shows["shows"][0]
    assert "guests" in shows["shows"][0]


def test_get_random_show():
    """Test /v2.0/shows/random route."""
    response = client.get(f"/v{API_VERSION}/shows/random")
    show = response.json()

    assert response.status_code == 200
    assert "id" in show
    assert "date" in show
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show


def test_get_random_show_date():
    """Test /v2.0/shows/random/date route."""
    response = client.get(f"/v{API_VERSION}/shows/random/date")
    _date = response.json()

    assert response.status_code == 200
    assert "date" in _date
    assert isinstance(_date["date"], str)


def test_get_random_show_id():
    """Test /v2.0/shows/random/id route."""
    response = client.get(f"/v{API_VERSION}/shows/random/id")
    _id = response.json()

    assert response.status_code == 200
    assert "id" in _id
    assert isinstance(_id["id"], int)


@pytest.mark.parametrize("year", [1998, 2020])
def test_get_random_show_by_year(year: int):
    """Test /v2.0/shows/random/year/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/random/year/{year}")
    show = response.json()

    assert response.status_code == 200
    assert "id" in show
    assert "date" in show
    assert str(year) in show["date"]
    assert "best_of" in show
    assert "repeat_show" in show
    assert "show_url" in show
    assert "original_show_id" in show
    assert "original_show_date" in show


@pytest.mark.parametrize("year", [9999])
def test_get_random_show_by_year_not_found(year: int):
    """Test /v2.0/shows/random/year/{year} route."""
    response = client.get(f"/v{API_VERSION}/shows/random/year/{year}")
    show = response.json()

    assert response.status_code == 404
    assert "detail" in show


def test_get_shows_recent():
    """Test /v2.0/shows/recent route."""
    response = client.get(f"/v{API_VERSION}/shows/recent")
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert "original_show_date" in shows["shows"][0]


def test_get_shows_repeat_best_ofs():
    """Test /v2.0/shows/repeat-best-ofs route."""
    response = client.get(f"/v{API_VERSION}/shows/repeat-best-ofs")
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert shows["shows"][0]["best_of"] is True
    assert "repeat_show" in shows["shows"][0]
    assert shows["shows"][0]["repeat_show"] is True
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert isinstance(shows["shows"][0]["original_show_id"], int)
    assert "original_show_date" in shows["shows"][0]
    assert isinstance(shows["shows"][0]["original_show_date"], str)


@pytest.mark.parametrize("inclusive", [True, False])
def test_get_shows_repeats(inclusive: bool):
    """Test /v2.0/shows/repeats route."""
    response = client.get(
        f"/v{API_VERSION}/shows/repeats", params={"inclusive": inclusive}
    )
    shows = response.json()

    assert response.status_code == 200
    assert "shows" in shows
    assert "id" in shows["shows"][0]
    assert "date" in shows["shows"][0]
    assert "best_of" in shows["shows"][0]
    assert "repeat_show" in shows["shows"][0]
    assert shows["shows"][0]["repeat_show"] is True
    assert "show_url" in shows["shows"][0]
    assert "original_show_id" in shows["shows"][0]
    assert isinstance(shows["shows"][0]["original_show_id"], int)
    assert "original_show_date" in shows["shows"][0]
    assert isinstance(shows["shows"][0]["original_show_date"], str)
