from app.db.mongo_client import MongoDBClient


class PostRepository:
    def __init__(self):
        self.collection = MongoDBClient().get_collection("posts")

    def insert_post(self, post_data: dict):
        query = {
            "source": post_data.get("source"),
            "collection_method": post_data.get("collection_method"),
            "title": post_data.get("title"),
            "author": post_data.get("author"),
            "created_at": post_data.get("created_at"),
            "text": post_data.get("text"),
        }

        existing = self.collection.find_one(query)

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

    def count_all(self):
        return self.collection.count_documents({})

    def count_by_source(self, source: str):
        return self.collection.count_documents({"source": source})

    def count_by_collection_method(self, method: str):
        return self.collection.count_documents({"collection_method": method})

    def get_top_topics(self, limit: int = 5):
        pipeline = [
            {"$group": {"_id": "$topic", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_top_authors(self, limit: int = 5):
        pipeline = [
            {"$match": {"author": {"$nin": [None, "", "nan"]}}},
            {"$group": {"_id": "$author", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_average_text_length(self):
        pipeline = [
            {
                "$project": {
                    "text_length": {
                        "$strLenCP": {
                            "$ifNull": ["$text", ""]
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "avg_text_length": {"$avg": "$text_length"}
                }
            }
        ]

        result = list(self.collection.aggregate(pipeline))
        if result:
            return round(result[0]["avg_text_length"], 2)
        return 0

    def get_source_breakdown(self):
        pipeline = [
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_method_breakdown(self):
        pipeline = [
            {"$group": {"_id": "$collection_method", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_posts_per_month(self):
        pipeline = [
            {
                "$match": {
                    "created_at": {"$nin": [None, "", "nan"]}
                }
            },
            {
                "$addFields": {
                    "created_at_date": {
                        "$dateFromString": {
                            "dateString": "$created_at",
                            "onError": None,
                            "onNull": None
                        }
                    }
                }
            },
            {
                "$match": {
                    "created_at_date": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$created_at_date"},
                        "month": {"$month": "$created_at_date"}
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))

    def get_posts_per_month_by_source(self):
        pipeline = [
            {
                "$match": {
                    "created_at": {"$nin": [None, "", "nan"]}
                }
            },
            {
                "$addFields": {
                    "created_at_date": {
                        "$dateFromString": {
                            "dateString": "$created_at",
                            "onError": None,
                            "onNull": None
                        }
                    }
                }
            },
            {
                "$match": {
                    "created_at_date": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$created_at_date"},
                        "month": {"$month": "$created_at_date"},
                        "source": "$source"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1,
                    "_id.source": 1
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))