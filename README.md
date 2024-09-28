<div align="right">
    <a href="https://www.buymeacoffee.com/bitArtisan">
        <img src="https://img.shields.io/badge/Buy_me_a_coffee-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee Pls!" />
    </a>
</div>

# rephraseX-Automatic-Twitter-Posting-Bot

## Overview

This Twitter bot automatically scrapes tweets and media from a specific user, it then rephrases the tweet content using Claude AI API (Anthropic) and reposts each tweet along with it's media attached to the provided authenticated user.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4367e6b1-36a0-499d-9bf8-3790435f2512" alt="Image Description" height=100px width=150px>
</p>

<p align="center"><strong><em>YouTube Caption Search Tool (CapScript)</em></strong></p>

## Features

- **Automatic Tweet Scraping:** Automatically finds the most recent tweets of a user and saves their content.
- **Image and Video Scraping from Twitter:** Downloads images and videos attached to tweets if any.
- **Rephrase Tweets:** Uses Claude AI to automatically rephrase tweets before posting them.
- **Selenium, BeautifulSoup4, and requests for Web Scraping:** Utilizes powerful web scraping libraries for efficient media extraction and interaction with web pages.
- **Organized Storage:** Automatically creates directories based on usernames and media types.
- **Error Handling:** Gracefully handles errors such as missing media or failed API requests.
- **Smart Anti-bot Detection Mechanism:** Bypasses common anti-bot measures by using headfull mode for webdriver manager (Firefox or Chrome).
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
Claude is an AI tool developed by Anthropic that can rephrase text. To use it, you need API keys:

1. **Sign Up for Anthropic API Access:**
   - Visit [Anthropic API](https://www.anthropic.com/) and sign up.
   
2. **Obtain an API Key:**
   - After registering, you will receive access to the Claude API. Retrieve your API key from the API dashboard.

## Prerequisites
Ensure you have the following installed:
- Python 3.10.x >=
- Pip (Python package installer)
- Twitter Developer API keys
- Claude API keys from Anthropic
- Selenium

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
## Usage

### 1. Add Twitter Authentication Details

You can either store your Twitter username and password in the `.env` file or provide them directly as command-line arguments when running the scraper.

#### Option 1: Storing credentials in `.env`

1. Create a `.env` file in the root directory of your project.
2. Add the following lines to the `.env` file:

    ```bash
    CONSUMER_KEY=your-consumer-key
    CONSUMER_SECRET=your-consumer-secret
    ACCESS_TOKEN=your-access-token
    ACCESS_TOKEN_SECRET=your-access-token-secret
    CLAUDE_API_KEY=your-claude-api-key
    TWITTER_USERNAME=your-twitter-username
    TWITTER_PASSWORD=your-twitter-password
    ```

3. After configuring the `.env` file, run the following command to scrape tweets:

    ```bash
    python scraper.py -t {number_of_tweets} -u {username}
    ```

    **Example:**

    ```bash
    python scraper.py -t 5 -u elonmusk
    ```

#### Option 2: Providing credentials as command-line arguments

Alternatively, you can provide your Twitter username and password directly in the command when running the scraper:

```bash
python scraper.py --user=@yourusername --password=yourpassword -t {number_of_tweets} -u {username}
```
## Contribution
We welcome contributions to this project! To contribute, follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Commit your changes and push them to your fork.
- Open a pull request to the main repository with a detailed explanation of your changes.
- 
## License and Legal Use
This project is licensed under the MIT License. However, please ensure your use of this bot complies with Twitter's Developer Agreement and Policy, and respect any intellectual property rights of the media you download and re-post. Always ensure you have permission to use any content you download before sharing it.

## Support Me
If you find RepoUp useful, consider supporting me by:

- Starring the repository on GitHub
- Sharing the tool with others
- Providing feedback and suggestions
- Follow me for more :)

<a href="https://www.buymeacoffee.com/bitArtisan"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=bitArtisan&button_colour=CBC3E3&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
<center>
    
---
For any issues or feature requests, please open an issue on GitHub. Happy coding!

<div style="text-align: center;">
  <p align="center">
    <img src="https://github.com/user-attachments/assets/36a3e590-bad2-463d-a25e-f56d65c26761" alt="octodance" width="100" height="100" style="margin-right: 10px;"/>
  </p>
</div>
</center>
