import os
from dotenv import load_dotenv
from pymongo import MongoClient
from functions import save_criteria_set
import pytest

def db():
    load_dotenv()
    pw = os.environ.get('MONGO_DB_PW')
    cluster = f"mongodb+srv://athielenhaus:{pw}@cluster0.opnz3cu.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(cluster)
    db = client.acc_db
    return db

def t_save_criteria_set(db):
    save_criteria_set(db, "a", "desc")
    criteria_sets = db.criteria
    search_result = criteria_sets.find({"name": "a", "description": "desc"})
    for result in search_result:
        assert (result["name"], result["description"]) == ("a", "desc")

db = db()
criteria_sets = db.criteria
results = criteria_sets.find({})
for result in results:
    print(result)
# t_save_criteria_set(db)