# WARNING: the code that follows will make you cry; a safety pig is provided below for your benefit.
#
#                          _
#  _._ _..._ .-',     _.._(`))
# '-. `     '  /-._.-'    ',/
#    )         \            '.
#   / _    _    |             \
#  |  a    a    /              |
#  \   .-.                     ;
#   '-('' ).-'       ,'       ;
#      '-;           |      .'
#         \           \    /
#         | 7  .__  _.-\   \
#         | |  |  ``/  /`  /
#        /,_|  |   /,_/   /
#           /,_/      '`-'

import tweepy
import datetime, time
import csv
import io
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Opens the .env file with keys 
load_dotenv()
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

twitter_auth_keys = {
        "consumer_key" : consumer_key,
        "consumer_secret" : consumer_secret,
        "access_token" : access_token,
        "access_token_secret" : access_token_secret
}

auth = tweepy.OAuthHandler(
        twitter_auth_keys["consumer_key"],
        twitter_auth_keys["consumer_secret"]
        )
auth.set_access_token(
        twitter_auth_keys["access_token"],
        twitter_auth_keys["access_token_secret"]
        )
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Creates a CSV file and adds relevant rows. 
csvFile = io.open('tweets.csv', 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['Tweet ID', 'User Name', 'Tweet Text', 'Polarity Score', 'Subjectivity Score'])

def sentiment_analyser_score(api):
    print('Please enter a sentence to score')
    sentence = input()
    analysis = SentimentIntensityAnalyzer()
    deadend = True
    for tweet in api.search_tweets(q="" + sentence + "-filter:retweets", count=100, lang="en", tweet_mode="extended"):
        if (datetime.datetime.now() - tweet.created_at).days < 7:
            print(f"\n{tweet.user.name}:{tweet.full_text}")
            vaderScore = analysis.polarity_scores(tweet.full_text)
            textblob = TextBlob(tweet.full_text)
            print("Blob Score:")
            print(textblob.sentiment.polarity, textblob.sentiment.subjectivity)
            print(f"\nVader Score:")
            print(vaderScore)
            print("----------------------------------------------------------------------------------------------")
            csvWriter.writerow([tweet.id, tweet.user.name, tweet.full_text.encode('utf-8'), vaderScore])
            time.sleep(1)

        else:
            deadend = False
            plt.title(f"{sentence} Polarity Scores")
            labels = 'Positive', 'Negative', 'Neutral'
            sizes = [vaderScore['pos'], vaderScore['neg'], vaderScore['neu']]
            explode = (0, 0.1, 0)
            sentimentGraph, graph = plt.subplots()
            graph.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%', shadow=True, startangle=90)
            graph.axis('equal')
            plt.show()
            return

        if not deadend:
            time.sleep(1)

sentiment_analyser_score(api)
csvFile.close()