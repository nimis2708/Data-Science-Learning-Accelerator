# db_utils.py
from pymongo import MongoClient
import pandas as pd
import os

# MongoDB connection setup
MONGO_URI = "mongodb+srv://misran:dsip@clusterdsip.hkfipy7.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDSIP"
DB_NAME = "docsDB"
COLLECTION_NAME = "documents"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# -----------------------------------
# Helper Functions
# -----------------------------------

def fetch_existing_filenames():
    """
    Fetch existing filenames from MongoDB collection.
    """
    existing_docs = collection.find({}, {"filename": 1, "_id": 0})
    existing_filenames = [doc.get("filename") for doc in existing_docs if doc.get("filename")]
    return existing_filenames

def check_for_duplicates(new_data):
    """
    Check if filenames in new_data already exist in MongoDB.
    """
    existing_filenames = fetch_existing_filenames()
    new_df = pd.DataFrame(new_data)

    if "GitHub Repo Name" in new_df.columns:
        # For GitHub Repo Name-based duplication checking
        new_df['Duplicate Status'] = new_df['GitHub Repo Name'].apply(
            lambda x: 'Duplicate' if x in existing_filenames else 'New'
        )
    elif "filename" in new_df.columns:
        new_df['Duplicate Status'] = new_df['filename'].apply(
            lambda x: 'Duplicate' if x in existing_filenames else 'New'
        )
    else:
        raise ValueError("Missing 'filename' or 'GitHub Repo Name' in input data.")

    return new_df.to_dict(orient='records')

def insert_new_records(new_data):
    """
    Insert only new filenames into MongoDB.
    """
    existing_filenames = fetch_existing_filenames()
    new_records = []

    for item in new_data:
        filename = item.get("GitHub Repo Name") or item.get("filename")
        if filename and filename not in existing_filenames:
            new_records.append({"filename": filename})

    if new_records:
        collection.insert_many(new_records)
        return {"inserted_count": len(new_records)}
    else:
        return {"inserted_count": 0}

def check_duplicate(data):
    """
    Check if a document with exact data already exists.
    """
    existing = collection.find_one(data)
    return existing is not None

def insert_document(data):
    """
    Insert a single document into MongoDB.
    """
    result = collection.insert_one(data)
    return str(result.inserted_id)


