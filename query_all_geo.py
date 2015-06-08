import json
from pymongo import MongoClient
import os
import time
import csv

start_time = time.time()
client = MongoClient()
db = client.sample_tweets

tweets_collection = db.sample_tweets_collection

query = {'geo' : {"$exists" : 1}, 
         'twitter_entities.media.media_url' : {"$exists" : 1}}
projection = {'actor.favoritesCount': 1, 
              'actor.followersCount' : 1, 
              'actor.friendsCount': 1,
              'actor.statusesCount': 1,
              'actor.link': 1,
              'twitter_entities.media.display_url': 1,
              'twitter_entities.media.media_url': 1,
              'geo.coordinates': 1,
              'postedTime': 1,
              'twitter_entities.media.sizes.large': 1,
              'location.country_code': 1,
              'location.name': 1,
              '_id' : 1}
meta_data = tweets_collection.find(query, projection)

meta = [m for m in meta_data]

data_file = [['display_url', 'media_url', 'size_h', 'size_w', 'lat', 'lon', 'favoritesCount', 'followersCount', 'friendsCount', 'statusesCount', 'profile_url', 'post_url', 'img_url', 'postedTime', 'location', 'country']]
for ind in range(len(meta)):
    try: display_url = meta[ind]['twitter_entities']['media'][0]['display_url']
    except: display_url = None
    try: media_url = meta[ind]['twitter_entities']['media'][0]['media_url']
    except: media_url = None
    try: size_h = meta[ind]['twitter_entities']['media'][0]['sizes']['large']['h']
    except: size_h = None
    try: size_w = meta[ind]['twitter_entities']['media'][0]['sizes']['large']['w']
    except: size_w = None
    try: lat = meta[ind]['geo']['coordinates'][0]
    except: lat = None
    try: lon = meta[ind]['geo']['coordinates'][1]
    except: lon = None
    try: favoritesCount = meta[ind]['actor']['favoritesCount']
    except: favoritesCount = None
    try: followersCount = meta[ind]['actor']['followersCount']
    except: follwoersCount = None
    try: friendsCount = meta[ind]['actor']['friendsCount']
    except: friendsCount = None
    try: statusesCount = meta[ind]['actor']['statusesCount']
    except: statusesCount = None
    try: profile_url = meta[ind]['actor']['link']
    except: profile_url = None
    try: post_url = meta[ind]['twitter_entities']['media'][0]['display_url']
    except: post_url = None
    try: img_url = meta[ind]['twitter_entities']['media'][0]['media_url']
    except: img_url = None
    try: postedTime = meta[ind]['postedTime']
    except: postedTime = None
    try: location = meta[ind]['location']['name']
    except: location = None
    try: country = meta[ind]['location']['country_code']
    except: country = None
    data_file.append([display_url, media_url, size_h, size_w, lat, lon, favoritesCount, followersCount, friendsCount, statusesCount, profile_url, post_url, img_url, postedTime, location, country])
    
rows = []
for item in data_file:
    rows.append([s.encode("utf-8") if isinstance(s,unicode) else s for s in item])
    
    
with open("output_sample_batch.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
    
end_time = time.time()

print "time elapsed", end_time - start_time