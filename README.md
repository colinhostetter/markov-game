# Markov's Revenge

A game built on Markov chains

## Running the app

This app requires Python 3.6+ and Node.js 6+.

To make it work, you first need to build the Markov chain, which is not included in source control because it is very large. The file `markov/raw_tweets.txt` is the raw corpus for the chain. It is a dump of several hundred thousand random English-language tweets, with retweets removed.

```
pip install -r requirements.txt
python markov/sanitizer.py        # Sanitize the raw tweets to normalize case, remove URLs and @mentions, etc.
python markov/markov_builder.py   # Build the Markov chains and dump them to JSON
```

This will generate two files, `markov.json` and `markov_mini.json`. The former is intended for production use, but it takes a long time to load because it is so large, so the latter is a much smaller version of the chain. It is intended for development but provides much less interesting gameplay.

Build client-side assets and run the app:

```
npm install
npm run build
python app_init.py
```

For production usage there are also systemd and nginx config files.

## Loading tweets

If you want to add more tweets to the markov chain you can just run the tweet loader, which will add raw tweets to the `raw_tweets.txt` file.

Set the `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN`, and `TWITTER_ACCESS_TOKEN_SECRET` environment variables and then run:

```
python markov/tweet_loader.py
```
