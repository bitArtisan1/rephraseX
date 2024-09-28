# rephraseX-Automatic-Twitter-Posting-Bot

This project automates the process of downloading images and videos from Twitter and posting rephrased tweets using the Claude AI API. It also includes progress tracking for media downloads and directory organization.

## Overview
This repository provides scripts to scrape media (images and videos) from Twitter, rephrase tweets using the Claude API, and post them on Twitter. Additionally, it offers features like progress tracking for media downloads and the ability to organize content into specific directories.

## Features
- **Image and Video Scraping from Twitter:** Download images and videos from tweet URLs.
- **Rephrase Tweets:** Use Claude AI to automatically rephrase tweets before posting them.
- **Progress Tracking for Downloads:** Shows real-time progress bars for media downloads.
- **Organized Storage:** Automatically creates directories based on usernames and media types.
- **Error Handling:** Gracefully handles errors such as missing media or failed API requests.
- **Rate Limiting:** Includes delays to avoid hitting Twitter's rate limits during automation.

## Obtaining Twitter API Keys
To interact with the Twitter API, you'll need API keys from your Twitter Developer account. Follow these steps:

1. **Create a Twitter Developer Account:**
   - Go to [Twitter Developer](https://developer.twitter.com/) and sign in.
   - Apply for a developer account by filling in the required information.

2. **Create a New App:**
   - After approval, go to the "Projects & Apps" section.
   - Click "Create App" and follow the steps to set up your app.
   
3. **Generate API Keys:**
   - In your app’s settings, navigate to "Keys and Tokens."
   - Copy your **Consumer Key**, **Consumer Secret**, **Access Token**, and **Access Token Secret**.

## Obtaining Claude API Keys
Claude is a powerful AI developed by Anthropic that can rephrase text. To use it, you need API keys:

1. **Sign Up for Anthropic API Access:**
   - Visit [Anthropic API](https://www.anthropic.com/) and sign up.
   
2. **Obtain an API Key:**
   - After registering, you will receive access to the Claude API. Retrieve your API key from the API dashboard.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Pip (Python package installer)
- Twitter Developer API keys
- Claude API keys from Anthropic
- Selenium for image scraping (optional, if you want to scrape images)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/twitter-media-downloader.git
   cd twitter-media-downloader
   ```
2. **Install the Required Dependencies:** Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```
3. **Set Up API Keys:**
- Create a `.env` file in the root directory of your project.
- Add the following lines to the `.env` file:
```bash
CONSUMER_KEY=your-consumer-key
CONSUMER_SECRET=your-consumer-secret
ACCESS_TOKEN=your-access-token
ACCESS_TOKEN_SECRET=your-access-token-secret
CLAUDE_API_KEY=your-claude-api-key
```
4. Install WebDriver for Selenium: If you're using the image scraping feature, install webdriver-manager for Selenium:

```bash
pip install webdriver-manager
```
## Usage
Download Images from Tweets: Use the Scrape_img.py script to download images from the specified tweet URLs:

bash
Copy code
python Scrape_img.py
Download Videos from Tweets: Use the twitter_downloader.py script to download videos from a list of Twitter URLs:

bash
Copy code
python twitter_downloader.py
Post Rephrased Tweets: Use the post.py script to authenticate with Twitter, rephrase tweets using the Claude API, and post them with media:

bash
Copy code
python post.py
Download Images and Videos with Progress Bars: Use the Downloader.py script to download images or videos with a progress bar:

bash
Copy code
python Downloader.py
Contribution
We welcome contributions to this project! To contribute, follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes and push them to your fork.
Open a pull request to the main repository with a detailed explanation of your changes.
License and Legal Use
This project is licensed under the MIT License. However, please ensure your use of this bot complies with Twitter's Developer Agreement and Policy, and respect any intellectual property rights of the media you download and re-post. Always ensure you have permission to use any content you download before sharing it.

Support Me
If you find this project helpful, consider supporting me:

Buy Me a Coffee
PayPal Donation
Thank you for your support!

