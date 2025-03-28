<div align="right">
    <a href="https://www.buymeacoffee.com/bitArtisan">
        <img src="https://img.shields.io/badge/Buy_me_a_coffee-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee Pls!" />
    </a>
</div>

# rephraseX-Automatic-Twitter-Posting-Bot

## Overview

This Twitter bot automatically scrapes tweets and media from a specific user, then rephrases the tweet content using an offline method powered by the Ollama platform and the Llama 3.2 model, and reposts each tweet along with its media attached to the provided authenticated user.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4367e6b1-36a0-499d-9bf8-3790435f2512" alt="Image Description" height=350px width=630px>
</p>

<p align="center"><strong><em>rephraseX-Automatic-Twitter-Posting-Bot</em></strong></p>

## Features

- **Automatic Tweet Scraping:** Automatically finds the most recent tweets of a user and saves their content.
- **Image and Video Scraping from Twitter:** Downloads images and videos attached to tweets if any.
- **Rephrase Tweets Offline:** Uses the Llama 3.2 model via Ollama to automatically rephrase tweets before posting them.
- **Selenium and BeautifulSoup4 for Web Scraping:** Utilizes powerful web scraping libraries for efficient media extraction and interaction with web pages.
- **Offline Rephrasing with Ollama:** Instead of API-based rephrasing, the bot uses Ollama to interact with local Llama 3.2 models for rephrasing tasks.
- **Organized Storage:** Automatically creates directories based on usernames and media types.
- **Error Handling and Robustness:** The bot includes many fallback mechanisms to gracefully handle errors such as missing media or failed scraping attempts.
- **Powerful Logger:** Built-in logger provides detailed logs of each action, allowing easy tracking and debugging.
- **Smart Anti-bot Detection Mechanism:** Bypasses common anti-bot measures by using headful mode for WebDriver Manager (Firefox or Chrome).
- **Rate Limiting:** Includes delays to avoid hitting Twitter's rate limits during automation.

## Transition from API to Offline Mode

~~### Obtaining Twitter API Keys~~  
~~To interact with the Twitter API, you must first obtain API keys from your Twitter Developer account. Below are the detailed steps:~~

~~### Step 1: Sign Up for a Twitter Developer Account~~  
~~1. Go to the [Twitter Developer Portal](https://developer.twitter.com/).~~  
~~2. Click on the "Apply" button to request access to the Twitter Developer platform.~~  
~~3. Fill out the required application form with details about how you intend to use the API. Be thorough and provide sufficient information, as Twitter reviews these applications manually.~~  
~~4. Once approved, you'll receive an email confirming your account creation.~~  

~~### Step 2: Create a New Project and App~~  
~~1. After your developer account is approved, log into the [Twitter Developer Dashboard](https://developer.twitter.com/en/portal/dashboard).~~  
~~2. Click on "Projects & Apps" in the top menu, then click the **Create Project** button.~~  
~~3. Choose an appropriate name for your project and specify how you will use the API (for example, "scraping tweets for analysis" or "media download").~~  
~~4. After creating the project, click **Create App** within the project dashboard. Name your app, and then Twitter will automatically create the required credentials.~~  

~~### Step 3: Generate API Keys and Tokens~~  
~~1. Inside your app's dashboard, navigate to the **Keys and Tokens** tab.~~  
~~2. Here, you will find your **API Key** (Consumer Key) and **API Secret Key** (Consumer Secret).~~  
~~3. Scroll down to the **Access Token & Access Token Secret** section. Click **Create** to generate an **Access Token** and **Access Token Secret**.~~  
~~4. Copy all four credentials (API Key, API Secret Key, Access Token, Access Token Secret) and store them securely. These are required for authenticating your app to interact with Twitter’s API.~~  

> **Important:** Never expose these keys publicly (e.g., in your source code or on GitHub). Store them securely in environment variables or a .env file.

### Transition to Offline Rephrasing with Ollama

While the bot previously relied on Twitter API keys for rephrasing, this version no longer uses API calls. Instead, **offline rephrasing** is powered by **Ollama** and the **Llama 3.2 model**. This change allows the bot to function without internet access for rephrasing tweets.

Here’s how to set it up:

### Step 1: Install Ollama  
You can install **Ollama** manually or use **Chocolatay** for installation.

#### Manual Installation  
1. Go to the [Ollama official website](https://www.ollama.com/) and download the installer for your platform (Windows/macOS/Linux).  
2. Follow the installation instructions provided on the site.

#### Installation via Chocolatay  
Alternatively, you can use the **Chocolatay** package manager to install Ollama easily by running the following command in your terminal:

```chocolatay install ollama```

### Step 2: Install the Llama 3.2 Model  
Once Ollama is installed, you can add the Llama 3.2 model to Ollama. 

#### Installing Llama 3.2  
1. After you have installed Ollama, open your terminal or command prompt.
2. Run the following command to download and install the Llama 3.2 model:

```ollama pull llama3.2```

This will download the model to your local machine, making it available for offline usage.

> **Note:** Ensure that you have sufficient storage space for the model, as it requires a decent amount of space on your local drive.

---

## Llama 3.2 Model Details

The Llama 3.2 model is a powerful language model designed for a variety of NLP tasks, including text generation, summarization, translation, and rephrasing. It can perform effectively on a range of text-based tasks, including the rephrasing of tweets in this bot.

| **Specification**        | **Details**                                |
|--------------------------|--------------------------------------------|
| **Model Name**            | Llama 3.2                                  |
| **Model Size**            | ~13GB                                      |
| **Max Tokens**            | 4096 tokens                                |
| **Architecture**          | Transformer-based model                   |
| **Training Data**         | Trained on a large corpus of text from diverse domains. |
| **Performance**           | High quality text generation and rephrasing with the ability to maintain context across multiple sentences. |
| **Offline Usage**         | Fully offline once installed via Ollama.    |
| **Supported Tasks**       | Text rephrasing, summarization, language modeling, question answering. |
| **Storage Space**         | Requires approximately 13 GB of free disk space for the full model. |

### Key Features of Llama 3.2:
- **Max Tokens**: Llama 3.2 can handle up to **4096 tokens** in a single processing request. This allows the model to manage long tweets or threaded conversations with ease.
- **Size**: The model is **13GB** in size, so ensure you have sufficient space on your machine for installation.
- **Performance**: Llama 3.2 is fine-tuned for multiple language processing tasks, making it ideal for the rephrasing tasks this bot performs.
- **Offline Functionality**: Once installed, you don’t need an internet connection to interact with the model, which is great for both privacy and performance.

---

## Prerequisites  
Ensure you have the following installed:  
- Python 3.10.x >=  
- Pip (Python package installer)  
- Ollama (for offline rephrasing)  
- Selenium  
- BeautifulSoup4  
- Requests  

## Installation

1. **Clone the Repository:**  

```
git clone https://github.com/bitArtisan1/rephraseX-Automatic-Twitter-Posting-Bot.git  
cd rephraseX-Automatic-Twitter-Posting-Bot
```

2. **Install the Required Dependencies:** Install the required Python libraries using pip:

```pip install -r requirements.txt```

## Usage

### 1. Add Twitter Authentication Details  

You can either store your Twitter username and password in the .env file or provide them directly as command-line arguments when running the scraper.

#### Option 1: Storing credentials in .env  

1. Create a .env file in the root directory of your project.  
2. Add the following lines to the .env file:

`TWITTER_USERNAME=your-twitter-username`  
`TWITTER_PASSWORD=your-twitter-password`

3. After configuring the .env file, run the following command to scrape tweets:

`python scraper.py -t {number_of_tweets} -u {username}`

**Example:**

```python scraper.py -t 5 -u elonmusk```

#### Option 2: Providing credentials as command-line arguments  

Alternatively, you can provide your Twitter username and password directly in the command when running the scraper:

```python scraper.py --user=@yourusername --password=yourpassword -t {number_of_tweets} -u {username}```

## Contribution  
We welcome contributions to this project! To contribute, follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Commit your changes and push them to your fork.
- Open a pull request to the main repository with a detailed explanation of your changes.

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
