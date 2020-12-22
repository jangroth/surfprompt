from unittest.mock import MagicMock, mock_open, patch

from freezegun import freeze_time
from hamcrest import assert_that, is_
from pytest import fixture, raises
from src.surfprompt.data_retriever import DataRetriever, InvalidConfigurationException


@fixture
def dr():
    obj = DataRetriever.__new__(DataRetriever)
    obj.api_key = "api_key"
    return obj


@fixture
def default_config():
    return {
        "spots": [
            {"name": "Elouera - The Wall", "latitude": -34.05, "longitude": 151.15}
        ],
        "source": {
            "url": "https://www.test.com",
            "sources": ["noaa"],
            "params": ["swellDirection"],
        },
    }


@patch("os.path.isfile", return_value=False)
def test_should_call_api_if_no_data(mock_isfile, dr, default_config):
    dr.config = default_config
    dr._call_api = MagicMock()

    dr.go()

    dr._call_api.assert_called_once()


@freeze_time("2020-10-10 11:00:00")
def test_should_create_api_request(dr, default_config):
    dr.config = default_config

    result = dr._create_api_request("123", default_config["spots"][0])

    assert_that(result.id, is_("123"))
    assert_that(result.method, is_("GET"))
    assert_that(result.url, is_("https://www.test.com"))
    assert_that(
        result.params,
        is_(
            {
                "params": ["swellDirection"],
                "source": ["noaa"],
                "start": 1602327600.0,
                "end": 1602932400.0,
                "lat": -34.05,
                "lng": 151.15,
            }
        ),
    )
    assert_that(result.headers, is_({"Authorization": "api_key"}))


def test_should_convert_spot_name_to_id(dr):
    assert_that(dr._spot_name_to_id("Elouera - The Wall"), is_("elouerathewall"))


@patch("builtins.open", mock_open(read_data="data"))
def test_should_read_api_key(dr):
    assert dr._read_api_key() == "data"


@patch("builtins.open", mock_open(read_data="data"))
def test_should_read_config(dr):
    assert dr._read_config() == "data"


@patch("builtins.open", side_effect=[Exception])
def test_should_fail_if_key_file_does_not_exist(mock, dr):
    with raises(InvalidConfigurationException):
        dr._read_api_key()


@patch("builtins.open", side_effect=[Exception])
def test_should_fail_if_config_file_does_not_exist(mock, dr):
    with raises(InvalidConfigurationException):
        dr._read_config()
