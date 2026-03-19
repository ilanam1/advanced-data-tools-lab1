
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "advanced_data_lab")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")