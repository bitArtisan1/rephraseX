import os
import sys
import argparse
import getpass
from twitter_scraper import Twitter_Scraper
from twitter_downloader import download_twitter_video
from post import authenticate_twitter, post_scraped_tweets, rephrase_text_with_claude

try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)


def main():
    try:
        parser = argparse.ArgumentParser(
            add_help=True,
            usage="python scraper [option] ... [arg] ...",
            description="Twitter Scraper is a tool that allows you to scrape tweets from Twitter without using Twitter's API.",
        )

        # Parsing Twitter credentials and arguments
        parser.add_argument("--mail", type=str, default=os.getenv("TWITTER_MAIL"), help="Your Twitter mail.")
        parser.add_argument("--user", type=str, default=os.getenv("TWITTER_USERNAME"), help="Your Twitter username.")
        parser.add_argument("--password", type=str, default=os.getenv("TWITTER_PASSWORD"), help="Your Twitter password.")
        parser.add_argument("-t", "--tweets", type=int, default=50, help="Number of tweets to scrape (default: 50)")
        parser.add_argument("-u", "--username", type=str, default=None, help="Twitter username to scrape.")
        parser.add_argument("-ht", "--hashtag", type=str, default=None, help="Twitter hashtag to scrape.")
        parser.add_argument("-ntl", "--no_tweets_limit", nargs="?", default=False, help="Scrape tweets without limit.")
        parser.add_argument("-q", "--query", type=str, default=None, help="Scrape tweets from a query or search.")
        parser.add_argument("-a", "--add", type=str, default="", help="Additional data to scrape and save in CSV.")
        parser.add_argument("--latest", action="store_true", help="Scrape latest tweets")
        parser.add_argument("--top", action="store_true", help="Scrape top tweets")

        args = parser.parse_args()

        # Load user credentials
        USER_MAIL = args.mail
        USER_UNAME = args.user
        USER_PASSWORD = args.password

        if USER_UNAME is None:
            USER_UNAME = input("Twitter Username: ")

        if USER_PASSWORD is None:
            USER_PASSWORD = getpass.getpass("Enter Password: ")

        print()

        # Validate scraping parameters
        tweet_type_args = []
        if args.username:
            tweet_type_args.append(args.username)
        if args.hashtag:
            tweet_type_args.append(args.hashtag)
        if args.query:
            tweet_type_args.append(args.query)

        additional_data = args.add.split(",")

        if len(tweet_type_args) > 1:
            print("Please specify only one of --username, --hashtag, or --query.")
            sys.exit(1)

        if args.latest and args.top:
            print("Please specify either --latest or --top, not both.")
            sys.exit(1)

        # Step 1: Scrape Tweets
        if USER_UNAME and USER_PASSWORD:
            scraper = Twitter_Scraper(
                mail=USER_MAIL, username=USER_UNAME, password=USER_PASSWORD
            )
            scraper.login()
            scraper.scrape_tweets(
                max_tweets=args.tweets,
                no_tweets_limit=args.no_tweets_limit if args.no_tweets_limit is not None else True,
                scrape_username=args.username,
                scrape_hashtag=args.hashtag,
                scrape_query=args.query,
                scrape_latest=args.latest,
                scrape_top=args.top,
                scrape_poster_details="pd" in additional_data,
            )

            # Collect scraped data
            usernames = [tweet['user'] for tweet in scraper.get_tweets() if tweet.get('user')]
            tweet_links = [tweet['tweet_link'] for tweet in scraper.get_tweets() if tweet.get('tweet_link')]
            tweet_content = [tweet['content'] for tweet in scraper.get_tweets() if tweet.get('content')]

            print("Scraped Tweet Content:", tweet_content)
            print("Scraped Tweet Links:", tweet_links)
            print("Scraped Usernames:", usernames)

            scraper.save_to_csv()

            # Step 2: Rephrase and Post Tweets
            # Authenticate Twitter for posting tweets
            client = authenticate_twitter(
                consumer_key=os.getenv("TWITTER_API_KEY"),
                consumer_secret=os.getenv("TWITTER_API_SECRET_KEY"),
                access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
            )

            # Format the scraped tweets into a structure for posting
            tweets_data = [{"text": content, "media_urls": []} for content in tweet_content]  # Add media if needed

            # Post rephrased tweets
            post_scraped_tweets(client, os.getenv("CLAUDE_API_KEY"), tweets_data)

            # Download videos from tweet links
            download_twitter_video(tweet_links, usernames)

            if not scraper.interrupted:
                scraper.driver.close()
        else:
            print("Missing Twitter username or password environment variables. Please check your .env file.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nScript Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
