import tweepy
import time
from decouple import config
from keep_alive import keep_alive

print("==========REPLIER-BOT==========")

CONSUMER_KEY = config("CONSUMER_KEY")
CONSUMER_SECRET = config("CONSUMER_SECRET")
ACCESS_KEY = config("ACCESS_KEY")
ACCESS_SECRET = config("ACCESS_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def get_last_seen_id():
    return api.mentions_timeline()[0].id


def reply(last_seen_id):
    print("Retrieving Tweets...", flush=True)
    new_lsi = last_seen_id
    try:
        for mention in tweepy.Cursor(api.mentions_timeline,
                                     since_id=last_seen_id,
                                     tweet_mode="extended").items():
            mention = mention._json
            new_lsi = mention["id"]
            if (new_lsi > last_seen_id) and ("#hello"
                                             in mention["full_text"].lower()):
                print("Found #hello!", flush=True)
                print("Responding back...", flush=True)
                api.update_status(
                    "@" + mention["user"]["screen_name"] + " Hello there, " +
                    mention["user"]["name"] + "!",
                    mention["id"],
                )
    except tweepy.RateLimitError:
        time.sleep(300)
    except tweepy.TweepError as e:
        print(e.api_code)
        print(e.reason)
    return new_lsi


# keeps a server running, even after replit tab is closed
keep_alive()
last_seen_id = get_last_seen_id()
while True:
    last_seen_id = max(last_seen_id, reply(last_seen_id))
    time.sleep(30)