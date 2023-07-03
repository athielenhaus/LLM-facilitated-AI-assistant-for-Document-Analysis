import os
from dotenv import load_dotenv
from pymongo import MongoClient

class CriteriaSet():
    pass


def connect_to_database():
    load_dotenv()
    pw = os.environ.get('MONGO_DB_PW')
    cluster = f"mongodb+srv://athielenhaus:{pw}@cluster0.opnz3cu.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(cluster)
    db = client.acc_db
    return db

def save_criteria_set(db, crit_set_name, crit_set_description):
    crit_set = {"name": crit_set_name, "description": crit_set_description}
    criteria_sets = db.criteria
    criteria_sets.insert_one(crit_set)

def import_criteria_set(db, crit_set_name):
    criteria_sets = db.criteria
    search_result = criteria_sets.find({"name": crit_set_name})
    crit_set = search_result[0]
    return crit_set
