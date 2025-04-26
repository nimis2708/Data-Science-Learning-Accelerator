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
