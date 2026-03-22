import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["advanced_data_lab"]
collection = db["posts"]

data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

if "extra" in df.columns:
    extra_df = pd.json_normalize(df["extra"])
    df = pd.concat([df.drop(columns=["extra"]), extra_df], axis=1)

df.to_csv("social_media_data.csv", index=False, encoding="utf-8-sig")
print("CSV exported successfully.")