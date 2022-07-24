import requests
from flight_search import Flight
FLIGHT = Flight()
FLIGHT_API = "https://api.sheety.co/e5eb2de5ab6ed0981f94ecd45bdcd8ab/flightDeals/prices"
PUT_REQ = "https://api.sheety.co/c04e657e12326c93fcf1bcda402a3ea0/flightDeals/prices"
class DataManager:
    def get_code(self):
        response = requests.get(url=FLIGHT_API)
        data = response.json()
        sheet_data = data['prices']
        return sheet_data

