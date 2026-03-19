from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

print("Connected!")

db = client["advanced_data_lab"]
collection = db["test_collection"]

result = collection.insert_one({"message": "It works!"})
print("Inserted ID:", result.inserted_id)