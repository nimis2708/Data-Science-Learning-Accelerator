# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from db_utils import check_for_duplicates, insert_new_records

app = FastAPI()

class GitHubRepoItem(BaseModel):
    GitHub_Repo_Name: str

@app.post("/check-duplicates")
def check_duplicates(items: List[GitHubRepoItem]):
    try:
        data = [{"GitHub Repo Name": item.GitHub_Repo_Name} for item in items]
        result = check_for_duplicates(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insert-new")
def insert_new(items: List[GitHubRepoItem]):
    try:
        data = [{"GitHub Repo Name": item.GitHub_Repo_Name} for item in items]
        result = insert_new_records(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI
from pydantic import BaseModel
from db_utils import check_duplicate, insert_document

app = FastAPI()

class DataModel(BaseModel):
    # Define your expected fields here
    name: str
    email: str

@app.post("/check-duplicate")
def api_check_duplicate(data: DataModel):
    data_dict = data.dict()
    is_duplicate = check_duplicate(data_dict)
    return {"duplicate": is_duplicate}

@app.post("/insert-document")
def api_insert_document(data: DataModel):
    data_dict = data.dict()
    doc_id = insert_document(data_dict)
    return {"inserted_id": doc_id}

@app.get("/")
def read_root():
    return {"message": "Hello from DSLA FastAPI backend!"}



