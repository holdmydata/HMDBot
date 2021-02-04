###Following the freeCodeCamp.org Tweet Visualization and Sentiment Analysis in Python - Full Tutorial ###

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, Cursor, API
import pandas as pd
import numpy as np
import cred

##Twitter Client##
class TwitterClient():
    def __init__(self, twitter_user=None, num_friends=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

###AUTH CLASS###
class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(cred.api_key, cred.api_secret_key)
        auth.set_access_token(cred.access_token, cred.access_token_secret)
        return auth

class TwitterStreamer():
#Class for streaming and processing live tweets
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        #This handles Twitter Auth and Connection to Twitter Stream API
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hashtag_list)

class TwitterListener(StreamListener):
#Basic Listener class that prints tweets received to stdout

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename


    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True
    def on_error(self, status_code):
        if status_code == 420:
            #Returning False in case of rate limit
            return False
        print(status_code)


if __name__ == "__main__":
    hash_tag_list = ['salads','salad','Taylor Farms']
    fetched_tweets_filename = "tweets.json"

    twitter_client = TwitterClient('ElonMusk')
    print(twitter_client.get_user_timeline_tweets(1))


    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    
