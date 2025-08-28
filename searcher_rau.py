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

    try:
        f = open("/data/rau.last")
        lastresult = int(f.read())
        f.close()
    except:
        lastresult = 0
    

    #get the epoch time in milliseconds
    datestring = str(int(time.time()*1000))
    datestring2 = str(int(time.time()*1000)+14*24*3600*1000)

    print("Datestring : " + datestring )
    print("Datestring2: " + datestring2 )

    main_url = "https://www.asklepios.com/details/sprechstunde/samediRenderer/content/0/fieldsets/09/fields/0/fields/teaser.json?q=teaser&from="+datestring+"&to="+datestring2+"&insurance_id=public&event_category_id=192280&event_type_id=499322"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6",
        "authority": "www.doctena.de",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "referrer": "https://www.asklepios.com/details/sprechstunde~ref=75a1077f-9404-41ce-a164-3bca011a84ea~coId=agzal-allg-roberta-rau~",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    }



# curl 'https://www.asklepios.com/details/sprechstunde/samediRenderer/content/0/fieldsets/09/fields/0/fields/teaser.json?q=teaser&from=1756394167726&to=1766938567726&insurance_id=public&event_category_id=192280&event_type_id=499322' \
#   -H 'accept: application/json, text/javascript, */*; q=0.01' \
#   -H 'accept-language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6' \
#   -H 'cache-control: no-cache' \
#   -b 'route=.1; HCLBSTICKY=0e6f458b745d53faa0340cfb4de95202|aLByw|aLByR' \
#   -H 'pragma: no-cache' \
#   -H 'priority: u=1, i' \
#   -H 'referer: https://www.asklepios.com/details/sprechstunde~ref=75a1077f-9404-41ce-a164-3bca011a84ea~coId=agzal-allg-roberta-rau~' \
#   -H 'sec-ch-ua: "Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Windows"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'sec-gpc: 1' \
#   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36' \
#   -H 'x-requested-with: XMLHttpRequest'




    req = requests.get(
        main_url,
        json=None,
        proxies=None,
        timeout=30,
        headers=headers,
    )
    print(req.text)
    json_object = json.loads(req.text)
    # print(json_object)

#     json_object = json.loads("""
#     {
#   "morning": {
#     "times": [
#       {
#         "time": "2025-09-11T09:30:00+02:00",
#         "timestamp": "1757575800000"
#       },
#       {
#         "time": "2025-09-11T10:30:00+02:00",
#         "timestamp": "1757579400000"
#       },
#       {
#         "time": "2025-09-12T09:30:00+02:00",
#         "timestamp": "1757662200000"
#       },
#       {
#         "time": "2025-10-16T09:30:00+02:00",
#         "timestamp": "1760599800000"
#       }
#     ]
#   },
#   "lunch": {
#     "times": [
#       {
#         "time": "2025-09-10T12:30:00+02:00",
#         "timestamp": "1757500200000"
#       },
#       {
#         "time": "2025-09-10T14:30:00+02:00",
#         "timestamp": "1757507400000"
#       },
#       {
#         "time": "2025-09-11T11:30:00+02:00",
#         "timestamp": "1757583000000"
#       },
#       {
#         "time": "2025-09-11T12:30:00+02:00",
#         "timestamp": "1757586600000"
#       }
#     ]
#   },
#   "afternoon": {
#     "times": [
#       {
#         "time": "2025-09-10T16:30:00+02:00",
#         "timestamp": "1757514600000"
#       },
#       {
#         "time": "2025-09-15T16:30:00+02:00",
#         "timestamp": "1757946600000"
#       },
#       {
#         "time": "2025-10-13T15:30:00+02:00",
#         "timestamp": "1760362200000"
#       },
#       {
#         "time": "2025-10-13T16:30:00+02:00",
#         "timestamp": "1760365800000"
#       }
#     ]
#   }
# }
#     """)
    #find the earliest timestamp in the json object
    ts = 0
    ts_hr = ""
    for part in ["morning", "lunch", "afternoon"]:
        for timeentry in json_object[part]["times"]:
            if ts == 0 or int(timeentry["timestamp"]) < ts:
                ts = int(timeentry["timestamp"])
                ts_hr = timeentry["time"]


    print("TSNOW:", ts)
    print("TSOLD:", lastresult)
    if ts != lastresult:
        print("Saving change")
        text_file = open("/data/rau.last", "w")
        text_file.write(str(ts))
        text_file.close()
        print("Sending mail")
        send_mail(
            smtp_to,
            "Rau Update: " + ts_hr,
            "Update auf https://www.asklepios.com/details/sprechstunde~ref=75a1077f-9404-41ce-a164-3bca011a84ea~coId=agzal-allg-roberta-rau~#b-appointment-route "
            + ts_hr,
            "Update auf https://www.asklepios.com/details/sprechstunde~ref=75a1077f-9404-41ce-a164-3bca011a84ea~coId=agzal-allg-roberta-rau~#b-appointment-route "
            + ts_hr,
        )


except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(smtp_to, "Exception searching for rau update ", text)
    print(str(E) + "\n\n" + traceback.format_exc())
