# db_utils.py
import os
from pymongo import MongoClient
import pandas as pd

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def get_db_collection():
    """
    Connect to MongoDB and return the collection.
    """
    if not MONGO_URI or not DB_NAME or not COLLECTION_NAME:
        raise ValueError("Missing MongoDB environment variables.")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection

def fetch_existing_filenames():
    """
    Fetch existing filenames from MongoDB collection.
    """
    collection = get_db_collection()
    existing_docs = collection.find({}, {"filename": 1, "_id": 0})
    existing_filenames = [doc.get("filename") for doc in existing_docs]
    return existing_filenames

def check_for_duplicates(new_data):
    """
    Check if filenames in new_data already exist in MongoDB.
    """
    existing_filenames = fetch_existing_filenames()
    new_df = pd.DataFrame(new_data)

    new_df['Duplicate Status'] = new_df['filename'].apply(
        lambda x: 'Duplicate' if x in existing_filenames else 'New'
    )
    return new_df.to_dict(orient='records')

def insert_new_records(new_data):
    """
    Insert only new filenames into MongoDB.
    """
    collection = get_db_collection()
    existing_filenames = fetch_existing_filenames()
    new_records = [item for item in new_data if item['filename'] not in existing_filenames]

    if new_records:
        collection.insert_many(new_records)
        return {"inserted_count": len(new_records)}
    else:
        return {"inserted_count": 0}

def check_duplicate(data):
    """
    Check if a document already exists.
    """
    collection = get_db_collection()
    existing = collection.find_one(data)
    return existing is not None

def insert_document(data):
    """
    Insert a single document into MongoDB.
    """
    collection = get_db_collection()
    result = collection.insert_one(data)
    return str(result.inserted_id)

