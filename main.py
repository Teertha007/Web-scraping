import smtplib
import ssl
import time
import sqlite3
import requests
import selectorlib

URL = "http://programmer100.pythonanywhere.com/tours/"
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

def scrape(url):
    response = requests.get(url)
    source = response.text
    return source


def extract_data(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    values = extractor.extract(source)["tours"]
    return values


def send_email(content):
    message = (f"""\
    Subject: New Tour Available!
    
    New tour available:
    {content}
    """
               .format(content))

    host = "smtp.gmail.com"
    port = 465

    username = "teertha.sarker.4@gmail.com"
    password = "bjfn pshp choo bbcp"

    receiver = "teertha.sarker.3@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
        print("Email sent successfully")


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor.execute("INSERT INTO events (band, city, date) VALUES (?, ?, ?)",
                   (band, city, date))
    connection.commit()



def read_file(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band,city,date = row
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scrape_data = scrape(URL)
        extracted = extract_data(scrape_data)
        print(extracted)


        if extracted != "No upcoming tours":
            row = read_file(extracted)
            if not row:
                store(extracted)
                send_email(extracted)
        time.sleep(2)
