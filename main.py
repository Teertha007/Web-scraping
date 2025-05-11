import requests
import selectorlib


URL = "http://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    response = requests.get(url)
    source = response.text
    return source

def extract_data(source):
    extractor =selectorlib.Extractor.from_yaml_file("extract.yaml")
    values = extractor.extract(source)["tours"]
    return values

def send_email():
    print("Email sent successfully!")

def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read_file(extracted):
    with open("data.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    scrape_data =scrape(URL)
    extracted =extract_data(scrape_data)
    print(extracted)

    content = read_file(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email()

