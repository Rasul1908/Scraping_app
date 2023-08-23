import time
import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3


ULR="https://programmer100.pythonanywhere.com/tours/"

connection=sqlite3.connect('sqldb.db')

def scrape(url):
    response=requests.get(url)
    source=response.text
    return source

def extract(source):
    extractor=selectorlib.Extractor.from_yaml_file("extract.yaml")
    value=extractor.extract(source)['tours']
    return value

def read(extracted):
    row=extracted.split(',')
    row=[item.strip() for item in row]
    band,city,date=row
    cursor = connection.cursor()

    cursor.execute("SELECT * from events WHERE band=? and city=? and date=?",(band,city,date))
    rows = cursor.fetchall()
    return rows

def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()

    cursor.execute("Insert into events values (?,?,?)",(band,city,date))
    connection.commit()

def send_email(message):
    host = 'smtp.gmail.com'
    port = 465
    username = 'webapptest1908@gmail.com'
    password = os.getenv("PASSWORD")
    receiver = username
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, msg=message)


if __name__=="__main__":
    while True:
        scraped=scrape(ULR)
        extracted=extract(scraped)
        print(extracted)

        if extracted != 'No upcoming tours':
                row = read(extracted)
                if not row:
                    store(extracted)
                    message ="Subject: Today's news. New event found" \
                             f"'\n' " \
                             f" {extracted}"
                    send_email(message=message)
                    time.sleep(3)





