from twikit import Client
import json
import os
from dotenv import load_dotenv
import time
import random

def extract_tweet_data(tweet):
    # Extract all attributes from the Tweet object as a dictionary    
    tweet_data = vars(tweet)

    # Filter out unwanted attributes if necessary
    keys_to_extract = ['id', 'full_text', 'created_at', 'lang', 'in_reply_to', 'media', 'urls', 'quote_count', 'reply_count', 'favorite_count', 'retweet_count', 'view_count', 'hashtags']
    filtered_tweet_data = {key: tweet_data[key] for key in keys_to_extract if key in tweet_data}
    
    return filtered_tweet_data

def login_to_twitter():
    client = Client('en-US')
    
    try:
        # Try to load the cookies
        client.load_cookies('cookies.json')

        print("[+] Loaded cookies. Successfully logged in.")
        return client
    except:
        print("[-] Failed to load cookies. Proceeding with login.")

        # Load environment variables
        USERNAME = os.getenv("USERNAME")
        EMAIL = os.getenv("EMAIL")
        PASSWORD = os.getenv("PASSWORD")

        # Create an instance of the client
        client = Client('en-US')

        client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
        print("[+] Logged in successfully.")

        # Save the cookies
        client.save_cookies('cookies.json')
        print("[+] Saved cookies.")

        return client

def get_tweets(client):
    total_tweets = 0
    tweets = client.get_user_tweets(os.getenv('TARGET_USER_ID'), 'Tweets', count=20)

    for tweet in tweets:
        tweet_content = extract_tweet_data(tweet)

        # print(tweet_content)

        # Save the tweet content to a JSON file
        json_file = json.dumps(tweet_content)
        with open('tweets.json', 'a') as f:
            f.write(json_file)
            f.write('\n')
    
    print("[+] Retrieved " + str(len(tweets)) + " Tweets")
    total_tweets += len(tweets)
    print("[+] Total Tweets: " + str(total_tweets))

    print("[+] Sleeping for 10-60 seconds")
    time.sleep(random.randint(10, 60))

    while True:
        print("[+] Getting more Tweets")
        more_tweets = tweets.next()
        tweets = more_tweets

        for tweet in more_tweets:
            tweet_content = extract_tweet_data(tweet)

            # print(tweet_content)

            # Save the tweet content to a JSON file
            json_file = json.dumps(tweet_content)
            with open('tweets.json', 'a') as f:
                f.write(json_file)
                f.write('\n')

        print("[+] Retrieved " + str(len(tweets)) + " Tweets")
        total_tweets += len(tweets)
        print("[+] Total Tweets: " + str(total_tweets))

        print("[+] Sleeping for 10-60 seconds")
        time.sleep(random.randint(10, 60))


if __name__ == '__main__':
    # Load the .env file
    print("[+] Loading .env file")
    config = load_dotenv(".env")

    # Login to Twitter
    print("[+] Logging in to Twitter")
    client = login_to_twitter()

    # Get Tweets
    print("[+] Getting Tweets")
    get_tweets(client)