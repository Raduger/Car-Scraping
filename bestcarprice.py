import os
import time
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from .utils import create_driver

load_dotenv()

def scrape_bestcarprice():
    user = os.getenv("BESTCARPRICE_USER")
    pwd = os.getenv("BESTCARPRICE_PASS")
    driver = create_driver()

    try:
        driver.get("https://app.bestcarprice.ch/login")
        time.sleep(3)

        driver.find_element(By.ID, "email").send_keys(user)
        driver.find_element(By.ID, "password").send_keys(pwd)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(5)

        driver.get("https://app.bestcarprice.ch/auctions")  # update URL
        time.sleep(5)

        cars = []
        listings = driver.find_elements(By.CSS_SELECTOR, ".auction-listing")

        for listing in listings:
            title = listing.find_element(By.CSS_SELECTOR, ".listing-title").text
            price = listing.find_element(By.CSS_SELECTOR, ".listing-price").text
            km = listing.find_element(By.CSS_SELECTOR, ".listing-km").text
            year = listing.find_element(By.CSS_SELECTOR, ".listing-year").text
            fuel = listing.find_element(By.CSS_SELECTOR, ".listing-fuel").text

            cars.append({
                "title": title,
                "price": price,
                "km": km,
                "year": year,
                "fuel": fuel,
                "source": "bestcarprice.ch"
            })

        return cars

    except Exception as e:
        print(f"[BestCarPrice] Error: {e}")
        return []
    finally:
        driver.quit()
