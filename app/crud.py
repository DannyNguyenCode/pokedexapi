from app.db import db
from google.cloud.firestore_v1 import FieldFilter
def create_user(data):
    email = data["email"].lower()
    doc_ref = db.collection('users').document()
    doc_ref.set(data)

    return {
        "message":f"User has registered successfully",
        "id":f"{doc_ref.id}",
        "email":f"{email}"
        }

def list_users():
    docs = db.collection('users').get()
    return docs

def get_user_by_id(id:str):
    return db.collection("users").document(id).get()

def update_user(id:str,data):
    db.collection("users").document(id).update(data)
    return {
        "message":f"user has been updated",
        }

def delete_user(id:str):
    db.collection("users").document(id).delete()
    return {"message":f"user has been deleted"}

def get_user_by_email(email:str):
    docs = db.collection("users").where(filter=FieldFilter("email","==",email.lower())).get()
    return docs

