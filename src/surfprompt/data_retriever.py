from os import path
from collections import namedtuple
import yaml

PATH_TO_DATA_FILE = path.join("data", "data.json")
PATH_TO_TIMESTAMP_FILE = path.join("data", ".last_update")
PATH_TO_CONFIG_FILE = path.join("config", "config.yaml")
PATH_TO_API_KEY_FILE = path.join("config", "api_key.txt")


class InvalidConfigurationException(Exception):
    pass


ApiRequest = namedtuple("ApiRequest", ["method", "url", "params", "headers"])


class DataRetriever:
    def __init__(self):
        self.api_key = self._read_api_key()
        self.config = self._read_config()

    def _read_api_key(self):
        try:
            with open(PATH_TO_API_KEY_FILE, "r") as api_key_file:
                api_key = api_key_file.read()
        except Exception as e:
            raise (
                InvalidConfigurationException(
                    f"Missing api key: {PATH_TO_API_KEY_FILE}"
                )
            ) from e

        return api_key

    def _read_config(self):
        try:
            with open(PATH_TO_CONFIG_FILE, "r") as config_file:
                config = yaml.safe_load(config_file)
        except Exception as e:
            raise (
                InvalidConfigurationException(
                    f"Missing config file: {PATH_TO_CONFIG_FILE}"
                )
            ) from e

        return config

    def _create_api_request(self):
        result = ApiRequest(
            "GET",
            self.config['source']['url'],
            {},
            {"Authorization": self.api_key},
        )
        return result

    def _call_api(self):
        pass

    def go(self):
        if not path.isfile(PATH_TO_DATA_FILE):
            self._call_api()


if __name__ == "__main__":
  DataRetriever()._create_api_request()
