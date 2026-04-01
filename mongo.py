import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

df = pd.read_csv("products.csv")
records = df.to_dict(orient="records")

collection.drop()
collection.insert_many(records)

print(f"✅ Inserted {len(records)} products into MongoDB.")
client.close()