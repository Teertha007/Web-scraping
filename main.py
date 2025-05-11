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

if __name__ == "__main__":
    scrape_data =scrape(URL)
    extracted =extract_data(scrape_data)
    print(extracted)
