import tweepy
import time
from decouple import config
from keep_alive import keep_alive

print("==========REPLIER-BOT==========")

CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
ACCESS_KEY = config('ACCESS_KEY')
ACCESS_SECRET = config('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def get_last_seen_id():
	last_id=None
	for status in api.user_timeline():
		last_id=status.id
		break
	return last_id

def retrieve_lsi(filename):
	try:
		with open(filename,'r') as f:
			last_seen_id=int(f.read().strip())
	except FileNotFoundError:
		created_file=open(filename, 'w')
		created_file.close()
		last_seen_id=get_last_seen_id()
		store_lsi(filename, last_seen_id)
	return last_seen_id

def store_lsi(filename,last_seen_id):
	with open(filename,'w') as f:
		f.write(str(last_seen_id))
	return

def reply():
	print("Retrieving Tweets...", flush=True)
	last_seen_id=retrieve_lsi('lastseenid.txt')
	try:
		mentions=api.mentions_timeline(last_seen_id, tweet_mode='extended')
		for mention in reversed(mentions):
			print(str(mention.id)+' - '+mention.full_text, flush=True)
			last_seen_id=mention.id
			store_lsi('lastseenid.txt',last_seen_id)
			if '#helloworld' in mention.full_text.lower():
				print('Found #helloworld!', flush=True)
				print('Responding back...', flush=True)
				api.update_status('@'+mention.user.screen_name+'#Helloworld back to you!', mention.id)
	except tweepy.RateLimitError:
		time.sleep(300)

# keeps a server running, even after replit tab is closed
keep_alive()

while True:
	reply()
	time.sleep(30)