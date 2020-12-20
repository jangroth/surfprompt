# import os
# import arrow
# import requests
# import json

# import yaml


# def call():
#     start = arrow.now().floor("hour")
#     end = start.shift(days=1)

#     response = requests.get(
#         "https://api.stormglass.io/v2/weather/point",
#         params={
#             "lat": -34.05,
#             "lng": 151.15,
#             "params": "swellDirection",
#             # "params": "swellDirection,swellHeight,swellPeriod,waveHeight,wavePeriod",
#             "source": "noaa",
#             "start": start.to("UTC").timestamp,  # Convert to UTC timestamp
#             "end": end.to("UTC").timestamp,  # Convert to UTC timestamp
#         },
#         headers={
#             "Authorization": ""
#         },
#     )

#     # Do something with response data.
#     json_data = response.json()

#     with open("data/data.json", "w") as outfile:
#         json.dump(json_data, outfile, indent=4, sort_keys=True)


# def update_last_update():
#     data = {"last_update_UTC": arrow.now().to("UTC").for_json()}
#     with open("data/.cache", "w") as outfile:
#         json.dump(data, outfile, indent=4, sort_keys=True)


# def seconds_since_last_update():
#     with open("data/.cache", "r") as data_file:
#         data = json.load(data_file)
#     last_update = arrow.get(data["last_update_UTC"])
#     now = arrow.now().to("UTC")
#     delta = now - last_update
#     return delta.seconds




# class SurfData:
#     def _data_already_exists(self):
#         data_file_exists = os.path.isfile(PATH_TO_DATA_FILE)
#         timestamp_file_exists = os.path.isfile(PATH_TO_TIMESTAMP_FILE)
#         return data_file_exists and timestamp_file_exists

#     def _invoke_api(self):
#         with open(PATH_TO_CONFIG_FILE, "r") as stream:
#             try:
#                 print(yaml.safe_load(stream))
#             except yaml.YAMLError as exc:
#                 print(exc)

#         pass

#     def _trigger_data_update_in_background(self):
#         pass

#     def _get_data(self):
#         pass

#     def retrieve(self):
#         if not (self._data_already_exists()):
#             self._invoke_api()
#         else:
#             self._trigger_data_update_in_background()
#         return self._get_data()


# if __name__ == "__main__":
#     print(SurfData().retrieve())
