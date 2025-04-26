# db_utils.py
from pymongo import MongoClient
import pandas as pd

# MongoDB setup
client = MongoClient("mongodb+srv://misran:<db_password>@clusterdsip.hkfipy7.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDSIP")  # <<=== Replace this with your real connection string
db = client["docsDB"]
collection = db["documents"]



def fetch_existing_filenames():
    """
    Fetch existing filenames from MongoDB collection.
    """
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
    existing_filenames = fetch_existing_filenames()
    new_records = [item for item in new_data if item['filename'] not in existing_filenames]

    if new_records:
        collection.insert_many(new_records)
        return {"inserted_count": len(new_records)}
    else:
        return {"inserted_count": 0}

from pymongo import MongoClient

def get_db_collection():
    client = MongoClient("mongodb+srv://misran:<db_password>@clusterdsip.hkfipy7.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDSIP")
    db = client["docsDB"]
    collection = db["documents"]
    return collection

def check_duplicate(data):
    collection = get_db_collection()
    existing = collection.find_one(data)
    return existing is not None

def insert_document(data):
    collection = get_db_collection()
    result = collection.insert_one(data)
    return str(result.inserted_id)

