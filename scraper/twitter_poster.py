import time
import os
import glob
from rich.panel import Panel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from logger import Logger
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--log-level=1")

class Twitter_Poster:
    def __init__(self, driver=None, username=None, password=None, mail=None):
        self.driver = driver
        self.username = username
        self.password = password
        self.mail = mail
        self.logged_in = False
        self.logger = Logger("TwitterPoster", "twitter_poster.log")

    def login(self):
        """Log in to Twitter"""
        if self.driver is None:
            self.logger.info("No driver provided. Using the default Chrome driver.")
            self.driver = webdriver.Chrome(options=chrome_options)

        try:
            # Open Twitter login page
            self.logger.info("Opening Twitter login page.")
            self.driver.get("https://twitter.com/i/flow/login")
            time.sleep(3)

            # Enter username (or email)
            self.logger.info("Locating username input field.")
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
            )
            username_value = self.username if self.mail is None else self.mail
            username_input.send_keys(username_value)
            username_input.send_keys(Keys.RETURN)
            time.sleep(2)

            # Handle optional username verification prompt
            try:
                self.logger.info("Checking for additional username verification prompt.")
                verify_username = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']"))
                )
                verify_username.send_keys(self.username)
                verify_username.send_keys(Keys.RETURN)
                time.sleep(2)
            except (TimeoutException, NoSuchElementException):
                self.logger.debug("No additional username prompt detected.")

            # Enter password
            self.logger.info("Locating password input field.")
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)

            # Wait until the home page loads
            self.logger.info("Waiting for home page to load after login.")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='AppTabBar_Home_Link']"))
            )

            self.logger.info("✅ Successfully logged in to Twitter!")
            self.logged_in = True
            return True

        except Exception as e:
            self.logger.error(f"❌ Login failed: {e}", exc_info=True)
            return False

    def post_tweet(self, text, media_paths=None, extra_media_wait=10):
        """
        Post a tweet with optional media attachments.

        Args:
            text (str): The tweet text.
            media_paths (list, optional): List of paths to media files.
            extra_media_wait (int, optional): Additional wait time for media uploads.
        """
        if not self.logged_in:
            self.logger.error("Not logged in. Please log in first.")
            return False

        try:
            self.logger.info("Navigating to Twitter home page.")
            self.driver.get("https://twitter.com/home")
            time.sleep(3)

            debug_dir = "./debug_screenshots"
            if not os.path.exists(debug_dir):
                os.makedirs(debug_dir)
                self.logger.info(f"Created debug directory: {debug_dir}")

            # Try clicking the compose tweet button if available
            try:
                compose_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='SideNav_NewTweet_Button']"))
                )
                compose_button.click()
                self.logger.info("Found and clicked the compose button.")
            except (TimeoutException, NoSuchElementException):
                try:
                    compose_area = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox' and @aria-label]"))
                    )
                    compose_area.click()
                    self.logger.info("Clicked on the compose area directly.")
                except (TimeoutException, NoSuchElementException):
                    self.logger.error("Could not find compose button. UI might have changed or you're already on the compose page.")

            time.sleep(2)

            # Locate the tweet input area
            try:
                tweet_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']"))
                )
                tweet_input.click()
                self.logger.info("Found tweet input area.")
            except (TimeoutException, NoSuchElementException):
                try:
                    tweet_input = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox' and @contenteditable='true']"))
                    )
                    tweet_input.click()
                    self.logger.info("Found tweet input with alternative selector.")
                except (TimeoutException, NoSuchElementException):
                    self.logger.error("Could not find tweet input field.")
                    self.driver.save_screenshot(f"{debug_dir}/no_tweet_input_{time.time()}.png")
                    raise Exception("Could not find tweet input field")

            time.sleep(1)

            # Enter tweet text
            tweet_input.send_keys(text)
            self.logger.info(f"Entered tweet text: {text[:30]}...")
            time.sleep(1)

            has_video = False
            has_media = False

            # Upload media if provided
            if media_paths and len(media_paths) > 0:
                valid_media_paths = []
                for media_path in media_paths:
                    if os.path.exists(media_path):
                        valid_media_paths.append(media_path)
                        if media_path.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                            has_video = True
                    else:
                        self.logger.warning(f"Media file does not exist: {media_path}")

                for media_path in valid_media_paths[:4]:
                    try:
                        media_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='fileInput']"))
                        )
                        absolute_path = os.path.abspath(media_path)
                        media_button.send_keys(absolute_path)
                        self.logger.info(f"Attached media: {media_path}")
                        has_media = True
                        time.sleep(2)
                        try:
                            upload_progress = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='progressBar']"))
                            )
                            self.logger.info(f"Upload in progress for: {media_path}")
                            WebDriverWait(self.driver, 60 if has_video else 30).until_not(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='progressBar']"))
                            )
                            self.logger.info(f"Media upload completed for: {media_path}")
                        except (TimeoutException, NoSuchElementException):
                            try:
                                WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='attachments']"))
                                )
                                self.logger.info(f"Media attachment confirmed for: {media_path}")
                            except (TimeoutException, NoSuchElementException):
                                self.logger.warning(f"Couldn't confirm media attachment for: {media_path}")
                    except Exception as e:
                        self.logger.error(f"Failed to attach media {media_path}: {e}", exc_info=True)
                        self.driver.save_screenshot(f"{debug_dir}/media_upload_failed_{time.time()}.png")
            else:
                self.logger.info("No media files to attach.")

            if has_video:
                extra_wait = extra_media_wait
                self.logger.info(f"Detected video upload - waiting extra {extra_wait} seconds for processing...")
                time.sleep(extra_wait)
                try:
                    processing_indicator = self.driver.find_element(By.XPATH, 
                        "//*[contains(text(), 'Processing') or contains(text(), 'Uploading')]")
                    if processing_indicator:
                        self.logger.info("Video still processing, waiting up to 60 more seconds...")
                        end_time = time.time() + 60
                        while time.time() < end_time:
                            try:
                                processing = self.driver.find_element(By.XPATH, 
                                    "//*[contains(text(), 'Processing') or contains(text(), 'Uploading')]")
                                self.logger.info("Still processing, waiting...")
                                time.sleep(5)
                            except NoSuchElementException:
                                self.logger.info("Processing complete!")
                                break
                except NoSuchElementException:
                    self.logger.info("No processing indicator found, proceeding.")

            self.driver.save_screenshot(f"{debug_dir}/before_post_button_{time.time()}.png")
            
            # Retry mechanism for clicking the Tweet/Post button
            tweet_button_enabled = False
            max_attempts = 10
            attempts = 0
            
            while not tweet_button_enabled and attempts < max_attempts:
                try:
                    tweet_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, 
                            "//*[contains(@data-testid, 'tweetButton') and not(@aria-disabled='true')]"))
                    )
                    # Scroll element into view
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", tweet_button)
                    # Try clicking using JavaScript
                    self.driver.execute_script("arguments[0].click();", tweet_button)
                    tweet_button_enabled = True
                    self.logger.info("Tweet button is enabled and clicked!")
                except ElementClickInterceptedException as e:
                    attempts += 1
                    self.logger.info(f"Tweet button click intercepted, retrying... (attempt {attempts}/{max_attempts})")
                    time.sleep(2)
                except (TimeoutException, NoSuchElementException):
                    attempts += 1
                    self.logger.info(f"Tweet button not enabled yet, waiting... (attempt {attempts}/{max_attempts})")
                    time.sleep(3)
            
            if not tweet_button_enabled and has_media:
                self.logger.warning("Tweet button may not be enabled but proceeding anyway...")

            # Fallback method if the retry loop did not click the button
            try:
                self.logger.info("Attempting to locate the Tweet/Post button with a combined XPath selector...")
                tweet_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(@data-testid, 'tweetButton') and (contains(., 'Tweet') or contains(., 'Post'))]"))
                )                
                self.driver.execute_script("arguments[0].click();", tweet_button)
                self.logger.info("Found the Tweet/Post button using combined XPath!")
                self.driver.execute_script("arguments[0].click();", tweet_button)
                self.logger.info("Clicked the button using JavaScript.")
                time.sleep(5)
                self.logger.success("Tweet posted successfully!")
                return True
            except Exception as e:
                self.logger.warning(f"Combined XPath selector fallback failed: {e}", exc_info = True)
                
            self.logger.error("❌ Failed to find and click the Tweet button")
            self.driver.save_screenshot(f"{debug_dir}/tweet_button_not_found_{time.time()}.png")
            return False

        except Exception as e:
            self.logger.error(f"❌ Failed to post tweet")
            debug_dir = "./debug_screenshots"
            if not os.path.exists(debug_dir):
                os.makedirs(debug_dir)
            self.driver.save_screenshot(f"{debug_dir}/post_failed_{time.time()}.png")
            return False


def post_tweets_with_selenium(poster, tweets_data, delay_between_tweets=60, keep_media=False, extra_media_wait=10):
    """
    Post rephrased tweets using Selenium browser automation.

    Args:
        poster: The Twitter_Poster instance.
        tweets_data: List of tweet data dictionaries.
        delay_between_tweets: Seconds to wait between tweets.
        keep_media: Whether to keep media files after posting.
        extra_media_wait: Additional seconds to wait for media uploads.
    """
    logger = Logger("PostTweets", "post_tweets.log")
    try:
        from twitter_rephraser import rephrase_text_with_ollama
        rephrase_function_available = True
        logger.info("Rephrase function found. Tweets will be rephrased.")
    except ImportError:
        logger.warning("Rephrase function not available. Using original text.")
        rephrase_function_available = False
    
    for i, tweet in enumerate(tweets_data, 1):
        tweet_text = tweet.get('text', '')
        if not tweet_text:
            logger.warning(f"Skipping tweet {i}: Empty text")
            continue
            
        panel_original = Panel(
            f"Original Tweet {i}: {tweet_text}",
            title=f"[bold cyan]Original Tweet {i}[/bold cyan]",
            style="cyan"
        )
        logger.console.print(panel_original)

        if rephrase_function_available:
            try:
                rephrased_text = rephrase_text_with_ollama(tweet_text)
                panel_rephrased = Panel(
                    f"Rephrased Tweet {i}: {rephrased_text}",
                    title=f"[bold green]Rephrased Tweet {i}[/bold green]",
                    style="green"
                )
                logger.console.print(panel_rephrased)
            except Exception as e:
                logger.error(f"Error rephrasing tweet {i}: {e}. Using original text instead.", exc_info=True)
                rephrased_text = tweet_text
        else:
            rephrased_text = tweet_text
            logger.info(f"Using original text for tweet {i} (rephrasing not available)")

        media_files = []
        has_video = False
        
        if 'user' in tweet and tweet['user'] and 'tweet_id' in tweet and tweet['tweet_id']:
            username = tweet['user']
            tweet_id = tweet['tweet_id']
            media_dir = f"./images/{username}"
            if os.path.exists(media_dir):
                logger.info(f"Looking for media files for tweet ID {tweet_id} from {username}")
                tweet_specific_media = []
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.mp4', '*.gif']:
                    tweet_specific_media.extend(glob.glob(os.path.join(media_dir, f"*_tweet{tweet_id}*{ext}")))
                    if ext == '*.mp4':
                        video_files = glob.glob(os.path.join(media_dir, f"*_tweet{tweet_id}*{ext}"))
                        if video_files:
                            has_video = True
                            logger.info(f"Detected video file(s) for tweet {tweet_id}")
                videos_dir = os.path.join(media_dir, "videos")
                if os.path.exists(videos_dir):
                    for ext in ['*.mp4', '*.mov', '*.avi', '*.webm']:
                        video_files = glob.glob(os.path.join(videos_dir, f"*_tweet{tweet_id}*{ext}"))
                        tweet_specific_media.extend(video_files)
                        if video_files:
                            has_video = True
                            logger.info(f"Detected video file(s) in videos directory for tweet {tweet_id}")
                if tweet_specific_media:
                    logger.info(f"Found {len(tweet_specific_media)} media files for tweet {tweet_id}")
                    for file in tweet_specific_media[:4]:
                        logger.info(f"  - {os.path.basename(file)}")
                    media_files = tweet_specific_media[:4]
                else:
                    logger.info(f"No media files found for tweet {tweet_id}")
            else:
                logger.info(f"No media directory found for user {username}")

        wait_time = extra_media_wait if has_video else 0
        
        success = poster.post_tweet(rephrased_text, media_files, extra_media_wait=wait_time)

        if success:
            logger.info(f"Tweet {i} posted successfully!")
        else:
            logger.error(f"Failed to post tweet {i}.")

        if not keep_media and media_files:
            for file_path in media_files:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        logger.info(f"Deleted media file: {file_path}")
                    except Exception as e:
                        logger.error(f"Failed to delete media file {file_path}: {e}", exc_info=True)

        if i < len(tweets_data):
            logger.info(f"Waiting {delay_between_tweets} seconds before posting next tweet...")
            time.sleep(delay_between_tweets)
