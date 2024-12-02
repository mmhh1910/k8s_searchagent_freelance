# Collects the most used tags on freelancermap projects

from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime
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

# Secrets
smtp_host = os.getenv("SMTP_HOST")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_to = os.getenv("SMTP_TO")
smtp_from = os.getenv("SMTP_FROM")

enable_email = True


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
    results = {}

    def delete_nr(s):
        return s.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    def replace(old, new, str, caseinsentive=True):
        if caseinsentive:
            return str.replace(old, new)
        else:
            return re.sub(re.escape(old), new, str, flags=re.IGNORECASE)

    def add(keyword):
        if keyword in [
            "IT Berater",
            '"IT Berater"',
            "projekt*",
            "Webdesign OR Webentwickler",
            "Berater -IT",
        ]:
            return
        keyword = keyword.lower()
        if keyword in results:
            results[keyword] = results[keyword] + 1
        else:
            results[keyword] = 1

    page = 1
    while True:
        time.sleep(1)
        foundonpage = 0
        # url = "https://www.freelancermap.de/projektboerse.html?cityName=&newQuery=&continents=&countries%5B%5D=1&states=&city=&radius=&query=kubernetes&created=30&contractTypes%5B0%5D=contract&contractTypes%5B1%5D=remote&categories%5B0%5D=11&excludeDachProjects=0&sort=1&pagenr={}"
        url = "https://www.freelancermap.de/projektboerse.html?cityName=&newQuery=&continents=&countries%5B%5D=1&states=&city=&radius=&query=&created=30&contractTypes%5B0%5D=contract&contractTypes%5B1%5D=remote&categories%5B0%5D=11&excludeDachProjects=0&sort=1&pagenr={}"
        # url = "https://www.freelancermap.de/projektboerse.html?contractTypes%5B0%5D=remote&endcustomer=0&created=30&excludeDachProjects=0&partner=&poster=&posterName=&lastRun=&currentPlatform=1&query=&queryParts=&continents=&countries%5B0%5D=1&states=&location=&radius=&city=&categories=&subCategories=&sort=1&pagenr={}"
        # url = "https://www.freelancermap.de/projektboerse.html?cityName=&newQuery=&continents=&countries%5B%5D=1&states=&city=&radius=&query=oracle&created=30&contractTypes%5B0%5D=remote&excludeDachProjects=0&sort=1&pagenr={}"
        main_url = url.format(page)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        }
        req = requests.get(main_url, headers=headers)
        bs = BeautifulSoup(req.text, "html.parser")

        keywords = bs.findAll("span", class_="keyword")

        for keyword in keywords:
            if "title" in keyword.attrs and keyword.attrs["title"] != None:
                words = keyword.attrs["title"]
                for w in words.split("<br/>"):
                    add(w)
            else:
                add(keyword.text)
            # add_entry(href, name, it, "freelancermap")
            foundonpage = foundonpage + 1

        if foundonpage <= 5:
            break
        page = page + 1
        if page > 200:
            break

    print("Pages seen: " + str(page - 1))
    sorted_dict = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    firstword = None
    for word in sorted_dict:
        if firstword == None:
            firstword = word
        if sorted_dict[word] < sorted_dict[firstword] / 40:
            break
        print(word + ": " + str(sorted_dict[word]))


except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(smtp_to, "Exception freelancermap_tags", text)
    print(str(E) + "\n\n" + traceback.format_exc())
