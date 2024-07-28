# TwitScraper

TwitScraper is a Python-based tool to scrape tweets from a specific Twitter user. It uses the `twikit` library to interact with the Twitter API and stores the retrieved tweets in a JSON file.

## Features

- Log in to Twitter using cookies or credentials.
- Retrieve tweets from a specified user.
- Extract and serialize tweet data including text, media, and user information.
- Save the tweet data to a JSON file.

## Requirements

- Python 3.6+
- `twikit` library
- `python-dotenv` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/notcoderguy/twitscraper.git
    cd twitscraper
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root by copying the example file:

    ```file
    # .env
    USERNAME=your_twitter_username
    EMAIL=your_twitter_email
    PASSWORD=your_twitter_password
    
    TARGET_USER_ID=target_twitter_user_id
    OR
    TARGET_USERNAME=target_twitter_username
    ```

## Usage

1. Run the `main.py` script:

    ```bash
    python main.py
    ```

2. Open the `tweets.json` file in a text editor to view the tweet data.

## Project Structure

```
twitscraper/
│
├── main.py                # Main script to run the application
├── requirements.txt       # List of required Python packages
├── .env                   # Environment variables (not included in the repo)
├── .env.example           # Example .env file
├── cookies.json           # Cookies for authentication
├── tweets.json            # JSON file containing the tweet data
└── README.md              # This README file
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.

## Acknowledgements

- [twikit](https://github.com/yourusername/twikit) for providing the API wrapper.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for managing environment variables.
