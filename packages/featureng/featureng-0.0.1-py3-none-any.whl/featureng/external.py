
import os
import json

import requests

from .exceptions import ApiRequestError, ApiResponseError


class OpenWeather:
    def __init__(self,key=None):
        """
        """
        if key is None:
            key = os.environ.get("OPEN_WEATHER_API_KEY")
        if key is None:
            raise AuthError("Open Weather API")
        self.key = key
        self.base_url = "https://api.census.gov/data/"

    def byCity(self,city,state_code=None,counry_code="US",start=None,end=None,cnt=None,type_="hour",):
        """
        """
        # Validate the location inputs
        if state_code is None:
            if city.count(",") != 2:
                raise ApiRequestError(
                    "Either specify `city`, `state_code` and `country_code` "
                    "or city should contain all 3, divided by commas."
                )
            q = city
        else:
            q = f"{city},{state_code},{country_code}"

        # Format the request url and params
        url = "http://history.openweathermap.org/data/2.5/history/city"
        params = {
            "q": q,
            "appid": self.key,
            "type": type_
        }
        # Add in optional params
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if cnt is not None:
            params["cnt"] = cnt

        # Try the request
        try:
            resp = requests.get(url,params=params)
        except Exception as e:
            raise ApiResponseError(str(e))
        data = resp.json()
        return data


class UsCensus:
    def __init__(self,key=None):
        """
        """
        if key is None:
            key = os.environ.get("US_CENSUS_API_KEY")
        if key is None:
            raise AuthError("US Census API")
        self.key = key
        self.base_url = "https://api.census.gov/data/"
