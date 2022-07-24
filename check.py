import requests
import datetime as dt

TOM_DATE = dt.datetime.now() + dt.timedelta(days=1)
TRAVEL_DATE = TOM_DATE + dt.timedelta(days=180)

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
FLIGHT_API = "L6df7ifSTk9vJ2xJhQZRC_D7Ine5TSzX"
query = {
        "fly_from": "LON",
        "fly_to": "NYC",
        "date_from": TOM_DATE.strftime("%d/%m/%Y"),
        "date_to": TRAVEL_DATE.strftime("%d/%m/%Y"),
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 28,
        "flight_type": "round",
        "one_for_city": 1,
        "max_stopovers": 0,
        "curr": "GBP"
    }

response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=FLIGHT_API, params=query)
data = response.json()['data']
print(data)
