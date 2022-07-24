# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
from pprint import pprint
from flight_search import Flight
from flight_data import FlightData
from data_manager import DataManager
from notification_manager import NotificationManager

notification = NotificationManager()
MIN_PRICE = float('inf')
dest = ""
message = ""

flight = Flight()
flight_data = DataManager()

FLIGHT_API = "https://api.sheety.co/e5eb2de5ab6ed0981f94ecd45bdcd8ab/flightDeals/prices"
PUT_REQ = "https://api.sheety.co/c04e657e12326c93fcf1bcda402a3ea0/flightDeals/prices"
response = requests.get(url=FLIGHT_API)
data = response.json()
sheet_data = data['prices']
for i in sheet_data:
    new_data = {
        "price": {
            "iataCode": flight.get_destination(i['city'])
        }
    }
    response = requests.put(
        url=f"{PUT_REQ}/{i['id']}",
        json=new_data)

# TODO flight data
import datetime as dt

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
FLIGHT_API = "L6df7ifSTk9vJ2xJhQZRC_D7Ine5TSzX"
TOM_DATE = dt.datetime.now() + dt.timedelta(days=1)
TRAVEL_DATE = TOM_DATE + dt.timedelta(days=180)
for i in sheet_data:
    location = f"{TEQUILA_ENDPOINT}/v2/search"
    query = {
        "fly_from": "LON",
        "fly_to": flight.get_destination(i['city']),
        "date_from": TOM_DATE.strftime("%d/%m/%Y"),
        "date_to": TRAVEL_DATE.strftime("%d/%m/%Y"),
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 28,
        "flight_type": "round",
        "one_for_city": 1,
        "max_stopovers": 0,
        "curr": "GBP"
    }
    header = {"apikey": FLIGHT_API}
    response = requests.get(url=location, headers=header, params=query)
    try:
        result = response.json()['data'][0]
        out_date = result["route"][0]["local_departure"].split("T")[0]
        return_date = result["route"][1]["local_departure"].split("T")[0]
        origin_city = result["route"][0]["cityFrom"]
        flight_data = FlightData(
            price=result["price"],
            origin_city=result["route"][0]["cityFrom"],
            origin_airport=result["route"][0]["flyFrom"],
            destination_city=result["route"][0]["cityTo"],
            destination_airport=result["route"][0]["flyTo"],
            out_date=result["route"][0]["local_departure"].split("T")[0],
            return_date=result["route"][1]["local_departure"].split("T")[0]
        )
        message = f"{flight_data.destination_city}: £{flight_data.price}"
    except IndexError:
        query["max_stopovers"] = 2
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=header,
            params=query,
        )
        data = response.json()["data"][0]
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][1]["cityTo"],
            destination_airport=data["route"][1]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T"),
            return_date=data["route"][2]["local_departure"].split("T"),
            stop_over=1,
            via_city=data["route"][0]["cityTo"]
        )
        pprint(f"{flight_data.destination_city}: £{flight_data.price} (Flight has {flight_data.stop_overs} stop over, via {flight_data.via_city}).")
    else:
        pprint(message)
    if MIN_PRICE > int(flight_data.price):
        MIN_PRICE = flight_data.price
        dest = flight_data.destination_city
        google_flight_link = f"https://www.google.co.uk/flights?hl=en#flt={flight_data.origin_airport}." \
                             f"{flight_data.destination_airport}.{flight_data.out_date}*{flight_data.destination_airport}." \
                             f"{flight_data.origin_airport}.{flight_data.return_date}"
# notification.send_notification(MIN_PRICE,origin_city,dest,out_date,return_date)

notification.send_email(MIN_PRICE, origin_city, dest, out_date, return_date,google_flight_link)
