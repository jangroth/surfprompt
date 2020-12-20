from os import path
from unittest.mock import MagicMock, patch, mock_open

from pytest import fixture
import pytest
from src.surfprompt.data_retriever import DataRetriever, InvalidConfigurationException


@fixture
def dr():
    obj = DataRetriever.__new__(DataRetriever)
    return obj


@patch("os.path.isfile", return_value=False)
def test_should_call_api_if_no_data(mock_isfile, dr):
    dr._call_api = MagicMock()

    dr.go()

    dr._call_api.assert_called_once()


@patch("builtins.open", mock_open(read_data="data"))
def test_should_read_api_key(dr):
    assert dr._read_api_key() == "data"


@patch("builtins.open", mock_open(read_data="data"))
def test_should_read_config(dr):
    assert dr._read_config() == "data"


@patch("builtins.open", side_effect=[Exception])
def test_should_fail_if_key_file_does_not_exist(mock, dr):
    with pytest.raises(InvalidConfigurationException):
        dr._read_api_key()


@patch("builtins.open", side_effect=[Exception])
def test_should_fail_if_config_file_does_not_exist(mock, dr):
    with pytest.raises(InvalidConfigurationException):
        dr._read_config()
