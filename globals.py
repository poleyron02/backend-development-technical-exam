import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
UPLOAD_DIR = '../storage/app/medalists/'
ARCHIVED_DIR = '../storage/app/archived/'
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = pymongo.MongoClient(MONGO_URL)
db = client['medalists_db']
collection = db['medalists']
