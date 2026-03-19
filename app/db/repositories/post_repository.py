from app.db.mongo_client import MongoDBClient


class PostRepository:
    def __init__(self):
        self.collection = MongoDBClient().get_collection("posts")

    def insert_post(self, post_data: dict):
        existing = None

        if post_data.get("url"):
            existing = self.collection.find_one({"url": post_data.get("url")})

        if existing:
            return None

        return self.collection.insert_one(post_data)

    def insert_many(self, posts: list[dict]):
        inserted_count = 0
        for post in posts:
            result = self.insert_post(post)
            if result is not None:
                inserted_count += 1
        return inserted_count

    def get_all(self):
        return list(self.collection.find({}, {"_id": 0}))

    def find_by_source(self, source: str):
        return list(self.collection.find({"source": source}, {"_id": 0}))

    def find_by_topic(self, topic: str):
        return list(self.collection.find({"topic": topic}, {"_id": 0}))