from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime, timedelta

import json
import os.path
from os import path
import time
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import traceback
import ssl

smtp_host = os.getenv("SMTP_HOST")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_to = os.getenv("SMTP_TO")
smtp_from = os.getenv("SMTP_FROM")
enable_email = True


try:

    def send_mail(
        to_email,
        subject,
        message,
        message_html=None,
        server=smtp_host,
        from_email=smtp_from,
    ):
        if enable_email:
            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = to_email
            msg["CC"] = to_email

            part1 = MIMEText(message, "plain")
            msg.attach(part1)
            if message_html != None:
                part2 = MIMEText(message_html, "html")            
                msg.attach(part2)
            # print("SMTP server: "+server)
            # print("SMTP username: "+smtp_username)
            server = smtplib.SMTP(server,587)
            server.ehlo()
            server.starttls(context=ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None))
            server.ehlo()
            # server.set_debuglevel(1)
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()

    

    main_url = "https://api.shore.com/v2/availability/calculate_slots"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "de-DE,de;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://connect.shore.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://connect.shore.com/",
        "sec-ch-ua": '"Brave";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "x-shore-origin": "booking-widget" 
    }



# curl 'https://api.shore.com/v2/availability/calculate_slots' \
#   -H 'accept: application/json, text/plain, */*' \
#   -H 'accept-language: de-DE,de;q=0.9' \
#   -H 'cache-control: no-cache' \
#   -H 'content-type: application/json;charset=UTF-8' \
#   -H 'origin: https://connect.shore.com' \
#   -H 'pragma: no-cache' \
#   -H 'priority: u=1, i' \
#   -H 'referer: https://connect.shore.com/' \
#   -H 'sec-ch-ua: "Brave";v="147", "Not.A/Brand";v="8", "Chromium";v="147"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Windows"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: same-site' \
#   -H 'sec-gpc: 1' \
#   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36' \
#   -H 'x-shore-origin: booking-widget' \
#   --data-raw '{"required_capacity":"1","search_weeks_range":0,"services_resources":[{"service_id":"001a3c48-6268-4a11-a479-4b8605274042"}],"timezone":"Europe/Berlin","starts_at":"2026-04-20 00:00:00","ends_at":"2026-04-21 23:59:59","merchant_id":"a665aea6-6989-4bc6-8c47-e1d5e44dfb5d"}'

    heute = datetime.now().strftime('%Y-%m-%d')

    
    morgen = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    data = {
        "required_capacity": "1",
        "search_weeks_range": 0,
        "services_resources": [
            {"service_id": "51ace01d-83fc-4382-ba35-e587ba3ae228"}
        ],
        "timezone": "Europe/Berlin",
        "starts_at": heute+" 00:00:00",
        "ends_at": morgen+" 23:59:59",
        "merchant_id": "974321fb-1ce5-4248-96a6-a57ab8b01277"
    }    


    req = requests.post(main_url, headers=headers, json=data)
    print(req.text)
    json_object = json.loads(req.text)
    
    # {"slots":[{"times":[],"date":"2026-04-20","id":"2026110"},{"times":[],"date":"2026-04-21","id":"2026111"}],"next_available_date":null,"slot_duration":15}
    if json_object["slots"][0]["times"] != []:
        print("Sending mail")
        send_mail(
            smtp_to,
            "Labor Update ",
            "Update auf https://www.meindirektlabor.de/termine/ "
            + req.text,
            "Update auf https://www.meindirektlabor.de/termine/ "
            + req.text,
        )


except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(smtp_to, "Exception searching for labor update ", text)
    print(str(E) + "\n\n" + traceback.format_exc())
