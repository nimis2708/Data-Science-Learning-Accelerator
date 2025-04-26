# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from db_utils import (
    check_for_duplicates,
    insert_new_records,
    check_duplicate,
    insert_document
)

app = FastAPI()

# --------------------------
# Models
# --------------------------

class GitHubRepoItem(BaseModel):
    GitHub_Repo_Name: str

class DataModel(BaseModel):
    name: str
    email: str

class InputData(BaseModel):
    input_data: str

# --------------------------
# Endpoints
# --------------------------

@app.get("/")
def read_root():
    return {"message": "Hello from DSLA FastAPI backend!"}

@app.post("/check-duplicates")
def api_check_duplicates(items: List[GitHubRepoItem]):
    try:
        data = [{"GitHub Repo Name": item.GitHub_Repo_Name} for item in items]
        result = check_for_duplicates(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insert-new")
def api_insert_new(items: List[GitHubRepoItem]):
    try:
        data = [{"GitHub Repo Name": item.GitHub_Repo_Name} for item in items]
        result = insert_new_records(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-duplicate")
def api_check_duplicate(data: DataModel):
    try:
        data_dict = data.dict()
        is_duplicate = check_duplicate(data_dict)
        return {"duplicate": is_duplicate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insert-document")
def api_insert_document(data: DataModel):
    try:
        data_dict = data.dict()
        doc_id = insert_document(data_dict)
        return {"inserted_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-data")
def api_process_data(input_data: InputData):
    try:
        data_dict = {"input_data": input_data.input_data}
        inserted_id = insert_document(data_dict)
        return {"result": f"Data inserted with ID: {inserted_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from db_utils import test_mongo_connection

@app.on_event("startup")
async def startup_event():
    test_mongo_connection()

