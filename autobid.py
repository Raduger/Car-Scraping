import os
import time
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from .utils import create_driver

load_dotenv()

def scrape_autobid():
    user = os.getenv("AUTOBID_USER")
    pwd = os.getenv("AUTOBID_PASS")
    driver = create_driver()

    try:
        driver.get("https://www.autobid.ch/login")
        time.sleep(3)

        driver.find_element(By.ID, "email").send_keys(user)
        driver.find_element(By.ID, "password").send_keys(pwd)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(5)

        driver.get("https://www.autobid.ch/auctions")  # update URL
        time.sleep(5)

        cars = []
        listings = driver.find_elements(By.CSS_SELECTOR, ".auction-item")

        for listing in listings:
            title = listing.find_element(By.CSS_SELECTOR, ".title").text
            price = listing.find_element(By.CSS_SELECTOR, ".price").text
            km = listing.find_element(By.CSS_SELECTOR, ".km").text
            year = listing.find_element(By.CSS_SELECTOR, ".year").text
            fuel = listing.find_element(By.CSS_SELECTOR, ".fuel").text

            cars.append({
                "title": title,
                "price": price,
                "km": km,
                "year": year,
                "fuel": fuel,
                "source": "autobid.ch"
            })

        return cars

    except Exception as e:
        print(f"[Autobid] Error: {e}")
        return []
    finally:
        driver.quit()
