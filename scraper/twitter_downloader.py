import os
import requests
import re
import bs4
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from alive_progress import alive_bar, config_handler
from tqdm import tqdm
from logger import Logger  # Our custom enhanced logger

from selenium.webdriver.chrome.options import Options


logger = Logger("MediaDownloader", "media_downloader.log")

def download_twitter_video(tweet_links, usernames):
    """Download media from tweet links"""
    if not tweet_links or len(tweet_links) == 0:
        logger.error("No tweet links provided for media download.")
        return

    logger.info(f"Extracting media from {len(tweet_links)} tweets...")

    # Create a Scrape instance to get image links from tweets
    scraper = TweetMediaScraper(tweet_links)
    image_links_by_tweet = scraper.get_image_links_by_tweet()

    # Check for videos in the tweets
    video_links_by_tweet = scraper.get_video_links_by_tweet()

    total_image_count = sum(len(links) for links in image_links_by_tweet.values())
    total_video_count = sum(len(links) for links in video_links_by_tweet.values())

    if total_image_count == 0 and total_video_count == 0:
        logger.error("No media found in the provided tweets.")
        return

    logger.info(f"Found {total_image_count} images and {total_video_count} videos across {len(tweet_links)} tweets.")

    # Download the images for each tweet
    for tweet_url, image_links in image_links_by_tweet.items():
        if not image_links:
            continue

        tweet_id = extract_tweet_id(tweet_url)
        # Determine username: use the index in tweet_links if possible, default otherwise.
        username_index = tweet_links.index(tweet_url) if tweet_url in tweet_links else 0
        username = usernames[username_index] if username_index < len(usernames) else "twitter_media"

        logger.info(f"Downloading {len(image_links)} image(s) for tweet ID: {tweet_id} from user: {username}")
        downloader = MediaDownloader(image_links)
        downloader.download(username, tweet_id)

    # Download the videos for each tweet
    for tweet_url, video_links in video_links_by_tweet.items():
        if not video_links:
            continue

        tweet_id = extract_tweet_id(tweet_url)
        username_index = tweet_links.index(tweet_url) if tweet_url in tweet_links else 0
        username = usernames[username_index] if username_index < len(usernames) else "twitter_media"

        logger.info(f"Downloading videos for tweet ID: {tweet_id} from user: {username}")
        for video_url in video_links:
            download_tweet_video(video_url, username, tweet_id)

    logger.info("Media downloaded successfully to images/ directory.")
    return

def extract_tweet_id(tweet_url):
    """Extract the tweet ID from a Twitter URL"""
    match = re.search(r'/status/(\d+)', tweet_url)
    if match:
        return match.group(1)
    return None

def download_video(url, file_name) -> None:
    """Download a video from a URL into a filename using an indeterminate spinner."""
    response = requests.get(url, stream=True)
    block_size = 1024  # 1KB
    download_path = file_name

    # Use the indeterminate spinner for downloads with unknown progress
    with open(download_path, "wb") as file, logger.indeterminate_spinner(f"Downloading {os.path.basename(file_name)}") as spinner:
        for data in response.iter_content(block_size):
            file.write(data)
            # Optionally, update spinner description if desired
            # spinner.set_description("Downloading...")
        spinner.set_description("Download complete!")
    
    logger.info(f"Video downloaded successfully to {download_path}!")


def download_tweet_video(url, username, tweet_id=None):
    """Download a Twitter video using an external service."""
    try:
        video_dir = f"./images/{username}/videos"
        os.makedirs(video_dir, exist_ok=True)
        
        api_url = f"https://twitsave.com/info?url={url}"
        response = requests.get(api_url)
        data = bs4.BeautifulSoup(response.text, "html.parser")

        download_button = data.find("div", class_="origin-top-right")
        quality_button = download_button.find("a") if download_button else None
        highest_quality_url = quality_button.get("href") if quality_button else None

        video_title_div = data.find("div", class_="leading-tight")
        file_name_p = video_title_div.find("p", class_="m-2") if video_title_div else None
        file_name = file_name_p.text if file_name_p else "video"

        file_name = re.sub(r"[^a-zA-Z0-9]+", '_', file_name).strip()
        if tweet_id:
            file_name = f"{file_name}_tweet{tweet_id}"
        file_name = f"{file_name}.mp4"

        if highest_quality_url:
            full_path = os.path.join(video_dir, file_name)
            download_video(highest_quality_url, full_path)
            return full_path
        else:
            logger.error(f"No valid video URL found for {url}")
            return None

    except Exception as e:
        logger.error(f"Failed to download video from {url}. Error: {e}", exc_info=True)
        return None

class TweetMediaScraper:
    def __init__(self, urls):
        self.urls = urls
        self.image_links_by_tweet = {}
        self.video_links_by_tweet = {}

    def get_image_links_by_tweet(self):
        """Get image links for each tweet URL"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--no-sandbox")

        try:
            logger.info("Setting up Chrome driver for media extraction (images)...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            for i, url in enumerate(self.urls, 1):
                logger.info(f"Processing tweet {i}/{len(self.urls)}: {url}")
                self.image_links_by_tweet[url] = self.get_images_from_tweet(driver, url)
            driver.quit()
            return self.image_links_by_tweet
        except Exception as e:
            logger.error(f"Error setting up Chrome driver for images: {e}", exc_info=True)
            return {}

    def get_video_links_by_tweet(self):
        """Get video links for each tweet URL"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--no-sandbox")

        try:
            logger.info("Setting up Chrome driver for media extraction (videos)...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            for i, url in enumerate(self.urls, 1):
                logger.info(f"Checking for videos in tweet {i}/{len(self.urls)}: {url}")
                self.video_links_by_tweet[url] = self.get_videos_from_tweet(driver, url)
            driver.quit()
            return self.video_links_by_tweet
        except Exception as e:
            logger.error(f"Error setting up Chrome driver for video extraction: {e}", exc_info=True)
            return {}

    def get_images_from_tweet(self, driver, tweet_url):
        """Extract image links from a tweet"""
        try:
            driver.get(tweet_url)
            time.sleep(5)
            images = driver.find_elements(By.CSS_SELECTOR, "img[src*='pbs.twimg.com/media']")
            links = [img.get_attribute('src') for img in images]
            if links:
                logger.info(f"Found {len(links)} images in tweet.")
            else:
                logger.info("No images found in tweet.")
            return links
        except Exception as e:
            logger.error(f"Error fetching images from {tweet_url}: {e}", exc_info=True)
            return []

    def get_videos_from_tweet(self, driver, tweet_url):
        """Extract video links from a tweet"""
        try:
            driver.get(tweet_url)
            time.sleep(5)
            videos = driver.find_elements(By.CSS_SELECTOR, "video")
            video_links = []
            if videos:
                logger.info(f"Found {len(videos)} video elements in tweet.")
                video_links = [tweet_url]
            else:
                video_players = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='videoPlayer']")
                if video_players:
                    logger.info(f"Found {len(video_players)} video players in tweet.")
                    video_links = [tweet_url]
                else:
                    logger.info("No videos found in tweet.")
            return video_links
        except Exception as e:
            logger.error(f"Error fetching videos from {tweet_url}: {e}", exc_info=True)
            return []

class MediaDownloader:
    def __init__(self, urls):
        self.urls = urls

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    def download(self, folder, tweet_id=None):
        if not os.path.exists("images"):
            os.makedirs("images")
            logger.info("Created 'images' directory")
        folder_path = f"images/{folder}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Created '{folder_path}' directory")

        logger.info(f"Downloading {len(self.urls)} media files for tweet {'ID: ' + tweet_id if tweet_id else ''}...")
        for i, link in enumerate(self.urls, 1):
            try:
                logger.info(f"Downloading file {i}/{len(self.urls)}")
                r = requests.get(link, allow_redirects=True, stream=True)
                if r.status_code != 200:
                    logger.error(f"Failed to download {link} - Status code: {r.status_code}")
                    continue
                base_filename = link.split("/")[-1].split('?')[0]
                if tweet_id:
                    filename_parts = os.path.splitext(base_filename)
                    sanitized_filename = f"{self.sanitize_filename(filename_parts[0])}_tweet{tweet_id}{filename_parts[1]}"
                else:
                    sanitized_filename = self.sanitize_filename(base_filename)
                file_path = os.path.join(folder_path, sanitized_filename)
                if not os.path.splitext(file_path)[1]:
                    file_path += ".jpg"

                total_size = int(r.headers.get('content-length', 0))
                block_size = 1024  # 1KB

                with open(file_path, 'wb') as f, \
                     logger.progress_bar(total=total_size if total_size > 0 else None, 
                                           description=f"Downloading {sanitized_filename[:25]}") as progress:
                    for data in r.iter_content(block_size):
                        f.write(data)
                        progress.update(advance=len(data))
                        
                logger.info(f"Downloaded: {file_path}")
            except Exception as e:
                logger.error(f"Error downloading {link}: {e}", exc_info=True)

        logger.info("Download complete.")
