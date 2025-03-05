import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from os import path
import os
import time
import smtplib
import traceback
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl


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

    spy = yf.Ticker('VWRL.AS').history(
        period='max',
        interval='1d'
    )

    #get the max value od the close column
    max_close = spy['Close'].max()

    #get the latest value of the close column
    latest_close = spy['Close'][-1]

    #get the second latest value of the close column    
    second_latest_close = spy['Close'][-2]

    #check if the latest value is 20% below the highest value   
    grenzwert = max_close * 0.8
    is_baerenmarkt=latest_close < grenzwert
    was_baerenmarkt=second_latest_close < grenzwert


    print(f'max close:              {max_close}')
    print(f'max close minus 20%     {grenzwert}')
    print(f'close yesterday:        {latest_close}')
    print(f'close the day before:   {second_latest_close}')

    if is_baerenmarkt!=was_baerenmarkt:
        if is_baerenmarkt:
            print('Seit heute Bärenmarkt')
            send_mail(
                smtp_to,
                "Seit heute Bärenmarkt",
                f'Seit heute Bärenmarkt!\n\nmax close:              {max_close}\nmax close minus 20%     {grenzwert}\nclose yesterday:        {latest_close}\nclose the day before:   {second_latest_close}\n\n',
            )

        else:
            print('Seit heute kein Bärenmarkt')
            send_mail(
                smtp_to,
                "Seit heute kein Bärenmarkt mehr",
                f'Seit heute kein Bärenmarkt!\n\nmax close:              {max_close}\nmax close minus 20%     {grenzwert}\nclose yesterday:        {latest_close}\nclose the day before:   {second_latest_close}\n\n',
            )
    else:
        send_mail(
            smtp_to,
            "Keine Änderung bezüglich Bärenmarkt",
            f'Keine Änderung bezüglich Bärenmarkt.\n\nmax close:              {max_close}\nmax close minus 20%     {grenzwert}\nclose yesterday:        {latest_close}\nclose the day before:   {second_latest_close}\n\n',
        )



except Exception as E:
    text = str(E) + "\n\n" + traceback.format_exc()
    send_mail(smtp_to, "Exception searching for baederland update ", text)
    print(str(E) + "\n\n" + traceback.format_exc())        