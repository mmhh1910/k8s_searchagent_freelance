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

# Secrets
smtp_host = os.getenv("SMTP_HOST")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_to = os.getenv("SMTP_TO")
smtp_from = os.getenv("SMTP_FROM")

# "Fixed" configurations
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
        f = open("/data/baederland1.last")
        lastresult1 = f.read()
        f.close()
    except:
        lastresult1 = ""
    try:
        f = open("/data/baederland2.last")
        lastresult2 = f.read()
        f.close()
    except:
        lastresult2 = ""

    tod = datetime.now()
    d = timedelta(days=-7)
    a = tod - d
    # datestring = a.strftime("%Y-%m-%d")
    datestring = "2023-07-05"

    main_url = "https://www.baederland.de/kurse/kursfinder/?course%5Blocation%5D=&course%5Blatlng%5D=&course%5Bpool%5D%5B%5D=17&course%5Bcategory%5D%5B%5D=60&course%5Bdate%5D=01.12.2023"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "de-DE,de;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "referrer": "https://www.baederland.de/kurse/kursfinder/?course%5Blocation%5D=&course%5Blatlng%5D=&course%5Bpool%5D%5B%5D=17&course%5Bcategory%5D%5B%5D=60&course%5Bdate%5D=25.12.2023",
    }

    req = requests.get(
        main_url,
        json=None,
        proxies=None,
        timeout=30,
        headers=headers,
    )
    print(req.text)
    if lastresult1 != req.text:
        text_file = open("/data/baederland1.last", "w")
        text_file.write(req.text)
        text_file.close()
        j = json.loads(req.text)
        html = j["#buchung"][0]["a"][0]
        # print(html)
        send_mail(
            smtp_to,
            "Baederland Update Aqua Rueckenfit",
            'Update auf <a href="'
            + main_url
            + '">Baederland Kurssuche</a> <p> '
            + html,
            html,
        )

except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(smtp_to, "Exception searching for baederland update ", text)
    print(str(E) + "\n\n" + traceback.format_exc())
