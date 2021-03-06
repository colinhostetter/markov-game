import os
import tweepy
from urllib3.exceptions import ProtocolError

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class LoaderStreamListener(tweepy.StreamListener):
    def __init__(self, *args, file_obj, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_obj = file_obj
        self.count = 0

    def on_status(self, status):
        if not hasattr(status, 'retweeted_status') and status.text[0:2] != 'RT':
            self.file_obj.write(status.text + '\n')
            self.count += 1
            if self.count % 1000 == 0:
                print(f'Wrote {self.count} tweets so far')

def load_tweets():
    with open('raw_tweets.txt', 'a', encoding='utf-8') as f:
        try:
            listener = LoaderStreamListener(file_obj=f)
            stream = tweepy.Stream(auth=api.auth, listener=listener)
            print('Streaming tweets...')
            stream.filter(languages=['en'], track=['a'])
        except ProtocolError:
            # tweepy doesnt handle this error properly
            print('hit error, retrying stream...')
            load_tweets()

if __name__ == '__main__':
    load_tweets()

