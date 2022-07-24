import requests

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
FLIGHT_API = "L6df7ifSTk9vJ2xJhQZRC_D7Ine5TSzX"
class Flight:
    def get_destination(self, city_name):
        location = f"{TEQUILA_ENDPOINT}/locations/query"
        query = {"term": city_name, "location_types": "city"}
        header = {"apikey": FLIGHT_API}
        response = requests.get(url=location, headers=header, params=query)
        result = response.json()["locations"]
        code = result[0]['code']
        return code
