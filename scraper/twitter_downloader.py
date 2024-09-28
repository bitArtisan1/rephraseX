import os
import re
import requests
import bs4
from tqdm import tqdm

def download_video(url, file_name) -> None:
    """Download a video from a URL into a filename."""
    response = requests.get(url, stream=True)

    block_size = 1024  # Size of each chunk in bytes
    download_path = file_name

    with open(download_path, "wb") as file:
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024, desc=f"Downloading {os.path.basename(file_name)}") as bar:
            for data in response.iter_content(block_size):
                file.write(data)
                bar.update(len(data))
    
    print(f"Video downloaded successfully to {download_path}!")

def create_directory_structure(base_directory, username):
    """Create the necessary directory structure to store videos."""
    if isinstance(username, list):
        # Join the list of usernames into a single string, separated by underscores or some delimiter
        username = "_".join(username)
        
    video_directory = os.path.join(base_directory, username, "videos")
    os.makedirs(video_directory, exist_ok=True)
    return video_directory

def download_twitter_video(urls, username, base_directory="media"):
    """Loop through a list of URLs to extract the highest quality video URL to download into a file, and create directory structure."""
    if not isinstance(urls, list):
        raise ValueError("Expected a list of URLs.")

    for url in urls:
        try:
            # Create the directory structure
            download_directory = create_directory_structure(base_directory, username)

            # Fetch video information from Twitter API
            api_url = f"https://twitsave.com/info?url={url}"
            response = requests.get(api_url)
            data = bs4.BeautifulSoup(response.text, "html.parser")

            # Attempt to find the download button and highest quality video URL
            download_button = data.find("div", class_="origin-top-right")
            quality_button = download_button.find("a") if download_button else None
            highest_quality_url = quality_button.get("href") if quality_button else None  # Highest quality video URL

            # Attempt to find the video file name
            video_title_div = data.find("div", class_="leading-tight")
            file_name_p = video_title_div.find("p", class_="m-2") if video_title_div else None
            file_name = file_name_p.text if file_name_p else "default_name"  # Default name in case of missing title

            # Clean the file name
            file_name = re.sub(r"[^a-zA-Z0-9]+", ' ', file_name).strip() + ".mp4"

            # Define the full path to save the video and download the video if the URL is valid
            if highest_quality_url:
                full_path = os.path.join(download_directory, file_name)
                download_video(highest_quality_url, full_path)
            else:
                print(f"No valid video URL found for {url}")

        except Exception as e:
            print(f"No video found for URL: {url}. Error: {str(e)}")
