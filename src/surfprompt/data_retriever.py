from collections import namedtuple
from datetime import datetime, timedelta, timezone
from os import path

import requests
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
        now_utc = datetime.now(tz=timezone.utc)
        a_week_from_now = now_utc + timedelta(days=7)
        result = ApiRequest(
            method="GET",
            url=self.config["source"]["url"],
            params={
                "lat": self.config["spots"][0]["latitude"],
                "lng": self.config["spots"][0]["longitude"],
                "params": self.config["source"]["params"],
                "source": self.config["source"]["sources"],
                "start": now_utc.timestamp(),
                "end": a_week_from_now.timestamp(),
            },
            headers={"Authorization": self.api_key},
        )
        return result

    def _call_api(self):
        # api_request = self._create_api_request()
        # response = requests.request(
        #     method=api_request.method,
        #     url=api_request.url,
        #     params=api_request.params,

        # )
        pass

    def go(self):
        if not path.isfile(PATH_TO_DATA_FILE):
            self._call_api()


if __name__ == "__main__":
    DataRetriever()._create_api_request()
