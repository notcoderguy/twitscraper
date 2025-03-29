import asyncio
from twikit import Client
import json
import os
from dotenv import load_dotenv
import random

def extract_tweet_data(tweet):
    # Extract all attributes from the Tweet object as a dictionary    
    tweet_data = vars(tweet)

    # Filter out unwanted attributes if necessary
    keys_to_extract = ['id', 'full_text', 'created_at', 'lang', 'in_reply_to', 'media', 'urls', 'quote_count', 'reply_count', 'favorite_count', 'retweet_count', 'view_count', 'hashtags']
    filtered_tweet_data = {key: tweet_data[key] for key in keys_to_extract if key in tweet_data}
    
    return filtered_tweet_data

def get_current_totp():
    """Generate and return current TOTP code using TOTP_KEY from environment"""
    import pyotp
    totp_key = os.getenv("X_TOTP_KEY")
    if not totp_key:
        raise ValueError("TOTP_KEY not found in environment variables")
    totp = pyotp.TOTP(totp_key)
    return totp.now()

async def login_to_twitter():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    import json
    import time

    client = Client('en-US')
    
    try:
        # Try to load the cookies
        client.load_cookies('cookies.json')
        print("[+] Loaded cookies. Successfully logged in.")
        return client
    except Exception as e:
        print("[-] Failed to load cookies. Proceeding with browser login. " + str(e))
        time.sleep(5)

        # Load environment variables
        X_USERNAME = os.getenv("X_USERNAME")
        X_EMAIL = os.getenv("X_EMAIL")
        X_PASSWORD = os.getenv("X_PASSWORD")

        # Set up Chrome browser with better error handling
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # Try installing ChromeDriver
            try:
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            except Exception as e:
                print(f"[-] ChromeDriver setup failed: {e}")
                print("[!] Trying alternative ChromeDriver path")
                driver = webdriver.Chrome(options=options)
                
        except Exception as e:
            print(f"[-] Failed to initialize Chrome: {e}")
            print("[!] Please ensure Google Chrome is installed:")
            print("    Linux: sudo apt install google-chrome-stable")
            print("    Mac: brew install --cask google-chrome")
            print("    Windows: Download from https://www.google.com/chrome/")
            exit(1)

        try:
            # Navigate to Twitter login
            driver.get("https://x.com/i/flow/login")

            # Wait for the page to load and wait for the login button to be present
            # time.sleep(5)
            
            # Wait for username field and enter credentials
            username_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_field.send_keys(X_USERNAME)
            driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]").click()

            # Wait for username field verification
            try:
                email_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "text"))
                )
                email_field.send_keys(X_EMAIL)
                driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]").click()
            except:
                print(f"[+] No email verification needed")
                pass

            # Wait for password field
            password_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.send_keys(X_PASSWORD)
            driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button").click()

            # Handle 2FA if needed
            try:
                code_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "text"))
                )
                code_field.send_keys(get_current_totp())
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button").click()
            except:
                pass  # No 2FA required

            # Wait for login to complete
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='/home']"))
            )

            # Get cookies and convert to twikit format
            selenium_cookies = driver.get_cookies()
            twikit_cookies = {}
            for cookie in selenium_cookies:
                twikit_cookies[cookie['name']] = cookie['value']
            
            # Save cookies in twikit-compatible format
            with open('cookies.json', 'w') as f:
                json.dump(twikit_cookies, f)

            print("[+] Browser login successful. Cookies saved.")
            driver.quit()

            # Load cookies into twikit client
            with open('cookies.json') as f:
                cookies = json.load(f)
                client.set_cookies(cookies)
            return client

        except Exception as e:
            print(f"[-] Browser login failed: {e}")
            driver.quit()
            exit(1)

async def get_tweets(client):
    total_tweets = 0
    try:
        tweets = await client.get_user_tweets(os.getenv('TARGET_USER_ID'), 'Tweets', count=20)
    except Exception as e:
        user = await client.get_user_by_screen_name(os.getenv('TARGET_USERNAME'))
        print("[+] User ID: " + str(user.id))
        tweets = await client.get_user_tweets(user.id, 'Tweets', count=20)

    for tweet in tweets:
        tweet_content = extract_tweet_data(tweet)

        print(tweet_content)

        # Save the tweet content to a JSON file
        json_file = json.dumps(tweet_content)
        with open('tweets.json', 'a') as f:
            f.write(json_file)
            f.write('\n')
    
    print("[+] Retrieved " + str(len(tweets)) + " Tweets")
    total_tweets += len(tweets)
    print("[+] Total Tweets: " + str(total_tweets))

    print("[+] Sleeping for 10-60 seconds")
    await asyncio.sleep(random.randint(10, 60))

    while True:
        print("[+] Getting more Tweets")
        more_tweets = await tweets.next()
        tweets = more_tweets

        for tweet in more_tweets:
            tweet_content = extract_tweet_data(tweet)

            print("[!] " + tweet_content)

            # Save the tweet content to a JSON file
            json_file = json.dumps(tweet_content)
            with open('tweets.json', 'a') as f:
                f.write(json_file)
                f.write('\n')

        print("[+] Retrieved " + str(len(tweets)) + " Tweets")
        total_tweets += len(tweets)
        print("[+] Total Tweets: " + str(total_tweets))

        print("[+] Sleeping for 10-60 seconds")
        await asyncio.sleep(random.randint(10, 60))

async def main():
    # Load the .env file
    print("[+] Loading .env file")
    load_dotenv(".env")

    # Login to Twitter
    print("[+] Logging in to Twitter")
    client = await login_to_twitter()

    # Get Tweets
    print("[+] Getting Tweets")
    await get_tweets(client)

if __name__ == '__main__':
    asyncio.run(main())
