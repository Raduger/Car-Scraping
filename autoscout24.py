import requests
from bs4 import BeautifulSoup

def scrape_autoscout(filters):
    url = "https://www.autoscout24.ch/de/autos/alle-marken"
    params = {
        "fregfrom": filters.get("year_min", 2012),
        "kmto": filters.get("km_max", 170000),
        "fuel": ",".join(filters.get("fuel", ["benzine", "diesel"])),
        "sort": "price_asc",
        "ustate": 3,
        "page": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.autoscout24.ch/",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[Autoscout24] Error fetching data: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    # Parse the cars from soup (adjust selectors as needed)
    cars = []
    for car_div in soup.select(".cl-list-element"):  # Example selector, adjust it
        title = car_div.select_one(".cldt-summary-makemodel").get_text(strip=True)
        price = car_div.select_one(".cldt-price").get_text(strip=True)
        cars.append({"title": title, "price": price})

    if not cars:
        print("No cars found or error scraping Autoscout24.")
    return cars

if __name__ == "__main__":
    filters = {"year_min": 2012, "km_max": 170000, "fuel": ["benzine", "diesel"]}
    results = scrape_autoscout(filters)
    if results:
        for car in results:
            print(car)
    else:
        print("No cars found or error scraping Autoscout24.")
