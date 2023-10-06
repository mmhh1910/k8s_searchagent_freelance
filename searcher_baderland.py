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

    main_url = "https://www.baederland-shop.de/kurse?_="
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "authority": "www.baederland-shop.de",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "de-DE,de;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.baederland-shop.de",
        "referer": "https://www.baederland-shop.de/kurse",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "x-phery": "1",
        "x-requested-with": "XMLHttpRequest",
    }

    data = (
        "args[kurskategorie_id]=8&args[kurstyp_id]=60&args[standort_id]=17&args[datum]="
        + datestring
        + "&phery[method]=POST&phery[submit_id]=kurse-filter&phery[remote]=get_kurse"
    )
    req = requests.post(
        main_url,
        data=data,
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
            'Update auf <a href="https://www.baederland-shop.de/kurse">https://www.baederland-shop.de/kurse</a> <p> '
            + html,
            html,
        )

    # data = (
    #     "args[kurskategorie_id]=3&args[kurstyp_id]=49&args[standort_id]=17&args[datum]="
    #     + datestring
    #     + "&phery[method]=POST&phery[submit_id]=kurse-filter&phery[remote]=get_kurse"
    # )
    # req = requests.post(
    #     main_url,
    #     data=data,
    #     json=None,
    #     proxies=None,
    #     timeout=30,
    #     headers=headers,
    # )
    # print(req.text)
    # if lastresult2 != req.text:
    #     text_file = open("/data/baederland2.last", "w")
    #     text_file.write(req.text)
    #     text_file.close()
    #     j = json.loads(req.text)
    #     html = j["#buchung"][0]["a"][0]
    #     # print(html)
    #     send_mail(
    #         smtp_to,
    #         "Baederland Update Aqua Gym Praevention",
    #         "Update auf https://www.baederland-shop.de/kurse ",
    #         'Update auf <a href="https://www.baederland-shop.de/kurse">https://www.baederland-shop.de/kurse</a> <p> '
    #         + html,
    #     )


except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(smtp_to, "Exception searching for baederland update ", text)
    print(str(E) + "\n\n" + traceback.format_exc())
