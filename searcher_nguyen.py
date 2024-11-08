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
            server = smtplib.SMTP(server)
            # server.set_debuglevel(1)
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()

    try:
        f = open("/data/nguyen.last")
        lastresult = int(f.read())
        f.close()
    except:
        lastresult = 0
    

    tod = datetime.now()
    d = timedelta(days=-7)
    a = tod - d
    datestring = a.strftime("%Y-%m-%d")

    main_url = "https://www.doctena.de/de/agendaSlot?from=1666389600&to=1666994399&language=de&weight=front_search_change_date&doctor=875357&reason=104688&agendaEid=2258c12e-fd91-490f-8eef-3d185ff88f20"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "de-DE,de;q=0.6",
        "authority": "www.doctena.de",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "referrer": "https://www.doctena.de/de/behandler/Dr_med_Lynhda_Nguyen-875357",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    }

    req = requests.post(
        main_url,
        json=None,
        proxies=None,
        timeout=30,
        headers=headers,
    )
    # print(req.text)
    json_object = json.loads(req.text)
    # print(json_object)
    ts = json_object["_embedded"]["agendas"][0]["_embedded"]["doctor"][
        "nextSlotTimestamp"
    ]
    ts_hr = json_object["_embedded"]["agendas"][0]["_embedded"]["doctor"]["nextSlot"][
        "date"
    ]
    print("TSNOW:", ts)
    print("TSOLD:", lastresult)
    if ts != lastresult:
        print("Saving change")
        text_file = open("/data/nguyen.last", "w")
        text_file.write(str(ts))
        text_file.close()
        print("Sending mail")
        send_mail(
            smtp_to,
            "Nguyen Update: " + ts_hr,
            "Update auf https://www.doctena.de/de/behandler/Dr_med_Lynhda_Nguyen-875357#15656 "
            + ts_hr,
            "Update auf https://www.doctena.de/de/behandler/Dr_med_Lynhda_Nguyen-875357#15656 "
            + ts_hr,
        )


except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(smtp_to, "Exception searching for nguyen update ", text)
    print(str(E) + "\n\n" + traceback.format_exc())
