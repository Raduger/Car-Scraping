import os
import time
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from .utils import create_driver

load_dotenv()

def scrape_carauktion():
    user = os.getenv("CARAUKTION_USER")
    pwd = os.getenv("CARAUKTION_PASS")
    driver = create_driver()

    try:
        driver.get("https://www.carauktion.ch/login")
        time.sleep(3)

        # Fill username/password - adjust IDs/names accordingly
        driver.find_element(By.ID, "loginEmail").send_keys(user)
        driver.find_element(By.ID, "loginPassword").send_keys(pwd)
        driver.find_element(By.ID, "loginButton").click()

        time.sleep(5)  # wait login

        driver.get("https://www.carauktion.ch/auction-listings")  # update to real URL
        time.sleep(5)

        cars = []
        listings = driver.find_elements(By.CSS_SELECTOR, ".auction-item")  # update selector

        for listing in listings:
            title = listing.find_element(By.CSS_SELECTOR, ".car-title").text
            price = listing.find_element(By.CSS_SELECTOR, ".car-price").text
            km = listing.find_element(By.CSS_SELECTOR, ".car-km").text
            year = listing.find_element(By.CSS_SELECTOR, ".car-year").text
            fuel = listing.find_element(By.CSS_SELECTOR, ".car-fuel").text

            cars.append({
                "title": title,
                "price": price,
                "km": km,
                "year": year,
                "fuel": fuel,
                "source": "carauktion.ch"
            })

        return cars

    except Exception as e:
        print(f"[Carauktion] Error: {e}")
        return []
    finally:
        driver.quit()
