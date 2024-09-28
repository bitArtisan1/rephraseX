from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class Scrape:
    def __init__(self, urls):
        self.urls = urls
        self.image_links = []

    def getImageLinks(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install())  # Update this with your chromedriver path
        driver = webdriver.Chrome(service=service, options=chrome_options)

        for url in self.urls:
            self.image_links.extend(self.get_images_from_tweet(driver, url))

        driver.quit()
        return self.image_links

    def get_images_from_tweet(self, driver, tweet_url):
        try:
            driver.get(tweet_url)
            time.sleep(5)  # Wait for the page to load (you might need to adjust this)
            
            images = driver.find_elements(By.CSS_SELECTOR, "img[src*='pbs.twimg.com/media']")
            return [img.get_attribute('src') for img in images]

        except Exception as e:
            print(f"Error fetching {tweet_url}: {e}")
            return []
