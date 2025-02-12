import requests
from bs4 import BeautifulSoup
import csv

URL = "<URL>"
OUTPUT_FILE = "scraped_data.csv"


def scrape_data():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to retrieve the data")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("div", class_="data-item")

    with open(OUTPUT_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Description"])

        for item in items:
            title = item.find("h2").text.strip()
            price = item.find("span", class_="price").text.strip()
            description = item.find("p").text.strip()
            writer.writerow([title, price, description])

    print(f"Data successfully scraped and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_data()
