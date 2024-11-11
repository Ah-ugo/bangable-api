from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url = os.getenv("MONGO_URL")

client = MongoClient(mongo_url)
db = client.bangable

users_db = db.users
videos_db = db.videos
comment_db = db.comments
channels_db =  db.channels
actors_db = db.actors
follow_db = db.follows
popular_video_db = db.popular_video
popular_user_db = db.popular_user
popular_channels_db = db.popular_channel
