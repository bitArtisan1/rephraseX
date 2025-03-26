import os
import sys
import logging
import pandas as pd
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from logger import Logger
from fake_headers import Headers
from tweet import Tweet
from scroller import Scroller

from selenium.webdriver.chrome.options import Options

TWITTER_LOGIN_URL = "https://twitter.com/i/flow/login"

# Suppress unwanted debug logs from Selenium and related libraries
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Twitter_Scraper:
    def __init__(
        self,
        mail=None,
        username=None,
        password=None,
        max_tweets=50,
        scrape_username=None,
        scrape_hashtag=None,
        scrape_query=None,
        scrape_poster_details=False,
        scrape_latest=True,
        scrape_top=False,
        proxy=None,
    ):
        # Initialize our logger instance
        self.logger = Logger("TwitterScraper", "twitter_scraper.log")
        self.logger.info("Initializing Twitter Scraper...")
        
        # Store credentials
        self.mail = mail
        self.username = username
        self.password = password
        self.interrupted = False
        self.tweet_ids = set()
        self.data = []
        self.tweet_cards = []
        self.scraper_details = {
            "type": None,
            "username": None,
            "hashtag": None,
            "query": None,
            "tab": None,
            "poster_details": False,
        }
        self.max_tweets = max_tweets
        
        self.router = self.go_to_home
        self.headless = False  # Non-headless mode for manual interaction
        self.driver = self._get_driver(proxy)
        self.actions = ActionChains(self.driver)
        self.scroller = Scroller(self.driver)
        self._config_scraper(
            max_tweets,
            scrape_username,
            scrape_hashtag,
            scrape_query,
            scrape_latest,
            scrape_top,
            scrape_poster_details,
        )

    def _config_scraper(
        self,
        max_tweets=50,
        scrape_username=None,
        scrape_hashtag=None,
        scrape_query=None,
        scrape_latest=True,
        scrape_top=False,
        scrape_poster_details=False,
    ):
        self.tweet_ids = set()
        self.data = []
        self.tweet_cards = []
        self.max_tweets = max_tweets
        self.scraper_details = {
            "type": None,
            "username": scrape_username,
            "hashtag": str(scrape_hashtag).replace("#", "") if scrape_hashtag is not None else None,
            "query": scrape_query,
            "tab": "Latest" if scrape_latest else "Top" if scrape_top else "Latest",
            "poster_details": scrape_poster_details,
        }
        self.router = self.go_to_home
        self.scroller = Scroller(self.driver)

        if scrape_username is not None:
            self.scraper_details["type"] = "Username"
            self.router = self.go_to_profile
        elif scrape_hashtag is not None:
            self.scraper_details["type"] = "Hashtag"
            self.router = self.go_to_hashtag
        elif scrape_query is not None:
            self.scraper_details["type"] = "Query"
            self.router = self.go_to_search
        else:
            self.scraper_details["type"] = "Home"
            self.router = self.go_to_home

    def _get_driver(self, proxy=None):
        self.logger.info("Setting up WebDriver...")
        header = Headers().generate()["User-Agent"]

        # Using FirefoxOptions for demonstration (you can switch to ChromeOptions if preferred)
        browser_option = FirefoxOptions()
        browser_option.add_argument("--no-sandbox")
        browser_option.add_argument("--disable-dev-shm-usage")
        browser_option.add_argument("--ignore-certificate-errors")
        browser_option.add_argument("--disable-gpu")
        browser_option.add_argument("--log-level=3")
        browser_option.add_argument("--disable-notifications")
        browser_option.add_argument("--disable-popup-blocking")
        browser_option.add_argument(f"--user-agent={header}")

        if proxy is not None:
            browser_option.add_argument(f"--proxy-server={proxy}")

        if self.headless:
            browser_option.add_argument("--headless")

        try:
            self.logger.info("Initializing WebDriver...")
            driver = webdriver.Firefox(options=browser_option)
            self.logger.info("WebDriver setup complete.")
            return driver
        except WebDriverException:
            try:
                self.logger.info("Downloading ChromeDriver as fallback...")
                chromedriver_path = ChromeDriverManager().install()
                chrome_service = ChromeService(executable_path=chromedriver_path)
                self.logger.info("Initializing ChromeDriver...")
                driver = webdriver.Chrome(service=chrome_service, options=browser_option)
                self.logger.info("WebDriver setup complete.")
                return driver
            except Exception as e:
                self.logger.error(f"Error setting up WebDriver: {e}")
                sys.exit(1)

    def login(self):
        self.logger.info("Logging in to Twitter...")
        try:
            self.driver.maximize_window()
            self.driver.get(TWITTER_LOGIN_URL)
            
            # Ask user for login method
            self.logger.info("Options:\n1. Manual login (recommended for troubleshooting)\n2. Automatic login (using provided credentials)")
            choice = input("Select login method (1 or 2): ")

            if choice == "2" and self.username and self.password:
                self.logger.info("Attempting automatic login...")
                self._attempt_automatic_login()
            else:
                self.logger.info("Manual login mode activated. Follow the instructions in the browser window.")
                input("\nPress Enter once you've successfully logged in...")

            # Verify login by checking cookies
            cookies = self.driver.get_cookies()
            auth_token = None
            for cookie in cookies:
                if cookie["name"] == "auth_token":
                    auth_token = cookie["value"]
                    break

            if auth_token is None:
                self.driver.get("https://twitter.com/home")
                sleep(3)
                cookies = self.driver.get_cookies()
                for cookie in cookies:
                    if cookie["name"] == "auth_token":
                        auth_token = cookie["value"]
                        break

                if auth_token is None:
                    self.logger.warning("Could not detect login token. Please verify if you're properly logged in.")
                    self.logger.info("Are you successfully logged in? (y/n): ")
                    confirm = input()
                    if confirm.lower() != 'y':
                        raise ValueError("Login unsuccessful. Please try again.")

            self.logger.info("Login Successful.")
        except Exception as e:
            self.logger.error(f"Login Failed: {e}")
            sys.exit(1)

    def _attempt_automatic_login(self):
        """Attempt to login automatically using stored credentials"""
        try:
            # Input username
            input_attempt = 0
            while input_attempt < 3:
                try:
                    username_field = self.driver.find_element("xpath", "//input[@autocomplete='username']")
                    username_field.send_keys(self.username)
                    username_field.send_keys(Keys.RETURN)
                    sleep(3)
                    break
                except NoSuchElementException:
                    input_attempt += 1
                    sleep(2)
            if input_attempt >= 3:
                self.logger.warning("Could not find username field. Switching to manual login.")
                return False

            # Input password
            input_attempt = 0
            while input_attempt < 3:
                try:
                    password_field = self.driver.find_element("xpath", "//input[@autocomplete='current-password']")
                    password_field.send_keys(self.password)
                    password_field.send_keys(Keys.RETURN)
                    sleep(3)
                    break
                except NoSuchElementException:
                    input_attempt += 1
                    sleep(2)
            if input_attempt >= 3:
                self.logger.warning("Could not find password field. Switching to manual login.")
                return False

            # Handle verification challenge if present
            try:
                self.driver.find_element("xpath", "//input[@data-testid='ocfEnterTextTextInput']")
                self.logger.info("Verification challenge detected. Please complete it manually.")
                input("\nPress Enter once you've completed the verification...")
            except NoSuchElementException:
                pass

            return True

        except Exception as e:
            self.logger.error(f"Error during automatic login: {e}")
            input("\nPress Enter to continue with manual login...")
            return False

    def go_to_home(self):
        self.driver.get("https://twitter.com/home")
        sleep(3)

    def go_to_profile(self):
        if not self.scraper_details["username"]:
            self.logger.error("Username is not set.")
            sys.exit(1)
        else:
            self.driver.get(f"https://twitter.com/{self.scraper_details['username']}")
            sleep(3)

    def go_to_hashtag(self):
        if not self.scraper_details["hashtag"]:
            self.logger.error("Hashtag is not set.")
            sys.exit(1)
        else:
            url = f"https://twitter.com/hashtag/{self.scraper_details['hashtag']}?src=hashtag_click"
            if self.scraper_details["tab"] == "Latest":
                url += "&f=live"
            self.driver.get(url)
            sleep(3)

    def go_to_search(self):
        if not self.scraper_details["query"]:
            self.logger.error("Query is not set.")
            sys.exit(1)
        else:
            url = f"https://twitter.com/search?q={self.scraper_details['query']}&src=typed_query"
            if self.scraper_details["tab"] == "Latest":
                url += "&f=live"
            self.driver.get(url)
            sleep(3)

    def get_tweet_cards(self):
        self.tweet_cards = self.driver.find_elements("xpath", '//article[@data-testid="tweet" and not(@disabled)]')

    def remove_hidden_cards(self):
        try:
            hidden_cards = self.driver.find_elements("xpath", '//article[@data-testid="tweet" and @disabled]')
            for card in hidden_cards[1:-2]:
                self.driver.execute_script("arguments[0].parentNode.parentNode.parentNode.remove();", card)
        except Exception as e:
            self.logger.warning(f"Error removing hidden cards: {e}")

    def scrape_tweets(
        self,
        max_tweets=50,
        no_tweets_limit=False,
        scrape_username=None,
        scrape_hashtag=None,
        scrape_query=None,
        scrape_latest=True,
        scrape_top=False,
        scrape_poster_details=False,
        router=None,
    ):
        self._config_scraper(
            max_tweets,
            scrape_username,
            scrape_hashtag,
            scrape_query,
            scrape_latest,
            scrape_top,
            scrape_poster_details,
        )
        router = router or self.router
        router()

        if self.scraper_details["type"] == "Username":
            self.logger.info(f"Scraping Tweets from @{self.scraper_details['username']}...")
        elif self.scraper_details["type"] == "Hashtag":
            self.logger.info(f"Scraping {self.scraper_details['tab']} Tweets from #{self.scraper_details['hashtag']}...")
        elif self.scraper_details["type"] == "Query":
            self.logger.info(f"Scraping {self.scraper_details['tab']} Tweets from {self.scraper_details['query']} search...")
        elif self.scraper_details["type"] == "Home":
            self.logger.info("Scraping Tweets from Home...")

        # Accept cookies to remove the banner
        try:
            accept_cookies_btn = self.driver.find_element("xpath", "//span[text()='Refuse non-essential cookies']/../../..")
            accept_cookies_btn.click()
        except NoSuchElementException:
            pass

        # Use logger's progress bar
        with self.logger.progress_bar(total=self.max_tweets, description="Scraping Tweets") as progress:
            refresh_count = 0
            added_tweets = 0
            empty_count = 0
            retry_cnt = 0

            while self.scroller.scrolling:
                try:
                    self.get_tweet_cards()
                    added_tweets = 0

                    for card in self.tweet_cards[-15:]:
                        try:
                            tweet_id = str(card)
                            if tweet_id not in self.tweet_ids:
                                self.tweet_ids.add(tweet_id)
                                if not self.scraper_details["poster_details"]:
                                    self.driver.execute_script("arguments[0].scrollIntoView();", card)

                                tweet = Tweet(
                                    card=card,
                                    driver=self.driver,
                                    actions=self.actions,
                                    scrape_poster_details=self.scraper_details["poster_details"],
                                )
                                if tweet and not tweet.error and tweet.tweet is not None:
                                    if not tweet.is_ad:
                                        self.data.append(tweet.tweet)
                                        added_tweets += 1
                                        progress.update(len(self.data))
                                        if len(self.data) >= self.max_tweets and not no_tweets_limit:
                                            self.scroller.scrolling = False
                                            break
                        except NoSuchElementException:
                            continue

                    if len(self.data) >= self.max_tweets and not no_tweets_limit:
                        break

                    if added_tweets == 0:
                        try:
                            while retry_cnt < 15:
                                retry_button = self.driver.find_element("xpath", "//span[text()='Retry']/../../..")
                                progress.update(total=len(self.data), description=f"Waiting... (Retry: {retry_cnt})")
                                sleep(58)
                                retry_button.click()
                                retry_cnt += 1
                                sleep(2)
                        except NoSuchElementException:
                            retry_cnt = 0
                            progress.update(len(self.data))

                        if empty_count >= 5:
                            if refresh_count >= 3:
                                self.logger.info("No more tweets to scrape.")
                                break
                            refresh_count += 1
                        empty_count += 1
                        sleep(1)
                    else:
                        empty_count = 0
                        refresh_count = 0

                except StaleElementReferenceException:
                    sleep(2)
                    continue
                except KeyboardInterrupt:
                    self.logger.warning("Keyboard Interrupt received.")
                    self.interrupted = True
                    break
                except Exception as e:
                    self.logger.error(f"Error scraping tweets: {e}")
                    break

        if len(self.data) >= self.max_tweets or no_tweets_limit:
            self.logger.info("Scraping Complete\n")
        else:
            self.logger.info("Scraping Incomplete\n")

        if not no_tweets_limit:
            self.logger.info(f"Tweets: {len(self.data)} out of {self.max_tweets}")

    def save_to_csv(self):
        self.logger.info("Saving Tweets to CSV...")
        now = datetime.now()
        folder_path = "./tweets/"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            self.logger.info(f"Created Folder: {folder_path}")

        data = {
            "Name": [tweet['user'] for tweet in self.data],
            "Handle": [tweet['handle'] for tweet in self.data],
            "Content": [tweet['content'] for tweet in self.data],
            "Tweet Link": [tweet['tweet_link'] for tweet in self.data],
        }

        # Use log_table to display the DataFrame preview
        headers = list(data.keys())
        rows = list(zip(*data.values()))[:5]  # Preview first 5 rows
        self.logger.log_table(headers, rows, title="Tweet Data Preview")

        df = pd.DataFrame(data)
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"{folder_path}{current_time}_tweets_1-{len(self.data)}.csv"
        pd.set_option("display.max_colwidth", None)
        df.to_csv(file_path, index=False, encoding="utf-8")
        self.logger.info(f"CSV Saved: {file_path}")

    def get_tweets(self):
        return self.data
