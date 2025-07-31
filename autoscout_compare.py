from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_autoscout():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.autoscout24.ch/de/autos/alle-marken")
    time.sleep(5)  # Wait for JavaScript to load

    results = []
    listings = driver.find_elements(By.CLASS_NAME, "cl-list-element")

    for listing in listings[:10]:
        try:
            title = listing.find_element(By.TAG_NAME, "h2").text
            price = listing.find_element(By.CLASS_NAME, "cldt-price").text
            results.append({"title": title, "price": price})
        except:
            continue

    driver.quit()
    return results
