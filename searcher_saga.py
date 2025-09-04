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



    main_url = "https://www.saga.hamburg/immobiliensuche?Kategorie=PARKING"
    headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "de-DE,de;q=0.5",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Brave\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "referrer": "https://www.saga.hamburg/immobiliensuche/allgemein/stellplaetze",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    }



    req = requests.get(
        main_url,
        json=None,
        proxies=None,
        timeout=30,
        headers=headers,
    )
    s=req.text.lower()
    print(req.text)

    if "gerstäcker" in s or "gerstaecker" in s or "neustadt" in s or "gerst&#228;cker" in s or "gerst&auml;cker" in s :
        print("Sending mail")
        send_mail(
            smtp_to,
            "Saga Update has Gerstäcker",
            "Update auf https://www.saga.hamburg/immobiliensuche?Kategorie=PARKING ",
            "Update auf https://www.saga.hamburg/immobiliensuche?Kategorie=PARKING "
        )


except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(smtp_to, "Exception searching for saga update ", text)
    print(str(E) + "\n\n" + traceback.format_exc())
