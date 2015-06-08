import json
from pymongo import MongoClient
import os
import time
src_path, data_type = "/data/myazdani/tweets/2014", ".json"

client = MongoClient()
db = client.sample_tweets

tweets_collection = db.sample_tweets_collection

 
json_paths = []  
for root, dirs, files in os.walk(src_path):
  json_paths.extend([os.path.join(root, f) for f in files if f.endswith(data_type)])

start_time = time.time()
num_tweets = 0

all_tweets = []
for k, json_path in enumerate(json_paths):
	tweets = []
	print k/float(len(json_paths))
	badTweets = []
	with open(json_path) as f:
		for i, activity in enumerate(f): 
			try:
				#ids.append(json.loads(activity)["id"])
				tweets.append(json.loads(activity))
			except:
				badTweets.append(activity)

	tweets.pop()
	if len(tweets) < 1: continue
	num_tweets += len(tweets)
	tweets_collection.insert(tweets)



end_time = time.time()

print "time elapsed", end_time - start_time