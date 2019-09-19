import mysql.connector
from mysql.connector import Error
import tweepy
import json
try:
    import json
except ImportError:
    import simplejson as json
# import simplejson as json
from dateutil import parser
import time
limit = 10
current = 0
consumer_key = 'Qx4adEOddt583YhzX3bxC8FD5'
consumer_secret = 'Hvf1cix75ZD9IWAcCNY9HhADJt9FyuLqTm9KE2DouFUp0D8KaC'
access_token = '1055619615898959877-UH48I8b7OTStEbE9P3gOOiiRDvw78H'
access_token_secret = 'HkdXBMspPIPbSQ7x2UWaq1ouIOJtTGWM5KqG9EgjtV9Hk'
password = 'twitterpwd@321'


def connect(username, created_at, tweet, retweet_count, place , location):
	"""
	connect to MySQL database and insert twitter data
	"""
	try:
		con = mysql.connector.connect(host = '166.62.26.1',
		database='harrytwitterdb', user='twitterusr', password = password, charset = 'utf8')
		

		if con.is_connected():
			"""
			Insert twitter data
			"""
			cursor = con.cursor()
			query = "INSERT INTO twitterdata (username, created_at, tweet, retweet_count,place, location) VALUES (%s, %s, %s, %s, %s, %s)"
			cursor.execute(query, (username, created_at, tweet, retweet_count, place, location))
			con.commit()
			
			
	except Error as e:
		print(e)

	cursor.close()
	con.close()

	return


# Tweepy class to access Twitter API
class Streamlistener(tweepy.StreamListener):
	def on_connect(self):
		print("You are connected to the Twitter API")


	def on_error(self):
		if status_code != 200:
			print("error found")
			# returning false disconnects the stream
			return False

	"""
	This method reads in tweet data as Json
	and extracts the data we want.
	"""
	def on_data(self,data):
		global current
		try:
			raw_data = json.loads(data)

			if 'text' in raw_data:
				 
				username = raw_data['user']['screen_name']
				created_at = parser.parse(raw_data['created_at'])
				tweet = raw_data['text']
				retweet_count = raw_data['retweet_count']

				if raw_data['place'] is not None:
					place = raw_data['place']['country']
					print(place)
				else:
					place = None
				

				location = raw_data['user']['location']

				#insert data just collected into MySQL database
				connect(username, created_at, tweet, retweet_count, place, location)
				print("Tweet colleted at: {} ".format(str(created_at)))
				#Loop to stop the program
				print(current, limit)
				current +=1
				if current == limit:
					return False
		except Error as e:
			print(e)


if __name__== '__main__':

	# # #Allow user input
	# track = []
	# while True:

	# 	input1  = input("what do you want to collect tweets on?: ")
	# 	track.append(input1)

	# 	input2 = input("Do you wish to enter another word? y/n ")
	# 	if input2 == 'n' or input2 == 'N':
	# 		break
	
	# print("You want to search for {}".format(track))
	# print("Initialising Connection to Twitter API....")
	# time.sleep(2)

	# authentification so we can access twitter
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api =tweepy.API(auth, wait_on_rate_limit=True)

	# create instance of Streamlistener
	listener = Streamlistener(api = api)
	stream = tweepy.Stream(auth, listener = listener)

	track = ['modi','tamil']
	#track = ['nba', 'cavs', 'celtics', 'basketball']
	# choose what we want to filter by
	stream.filter(track = track, languages = ['en'])

def start():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api =tweepy.API(auth, wait_on_rate_limit=True)

	# create instance of Streamlistener
	listener = Streamlistener(api = api)
	stream = tweepy.Stream(auth, listener = listener)

	track = ['trump','nasa']
	#track = ['nba', 'cavs', 'celtics', 'basketball']
	# choose what we want to filter by
	stream.filter(track = track, languages = ['en'])
