from twilio.rest import Client
import smtplib
import os
import requests

MY_EMAIL = "manishsutradhar66@gmail.com"
PASS = "eaxuxultrnisoscv"
USER_API = "https://api.sheety.co/e5eb2de5ab6ed0981f94ecd45bdcd8ab/usersDetail/sheet2"

class NotificationManager:
    def send_notification(self, price, cur_city, to_city, go_date, comeback_date):
        account_sid = 'AC270aa42ce63d664ad7f058442837fe95'
        auth_token = 'eeac0e82b53590a74309956a3e9901a7'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=f"Low price alert! Only £{price} to fly from {cur_city} to {to_city}, "
                 f"from {go_date} to {comeback_date} ",
            from_='+19035688002',
            to='+918638106504'
        )

    def send_email(self, price, from_city, to_city, from_date, to_date, google_flight_link):
        response = requests.get(url=USER_API)
        data = response.json()['sheet2']
        for i in data:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASS)
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=f"{i['email']}",
                                    msg=f"Subject:Flight details\n\nLow price alert! Only £{price} to fly from "
                                        f"{from_city} to {to_city} from {from_date} to {to_date}.\n{google_flight_link}".encode('utf-8'))

