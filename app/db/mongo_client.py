from pymongo import MongoClient
from app.config.settings import MONGO_URI, DB_NAME


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]