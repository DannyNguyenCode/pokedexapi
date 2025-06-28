from app.db import db
from google.cloud.firestore_v1 import FieldFilter
def create_user(data):
    email = data.get("email", "").lower()
    if not email:
        raise ValueError("Email is required")
    data["email"] = email

    doc_ref = db.collection('users').document()
    user_uid = {'id': doc_ref.id}
    full_data = user_uid | data

    doc_ref.set(full_data)

    return {
        "message": "User has registered successfully",
        "id": doc_ref.id,
        "email": email
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

def get_pokemons_by_user_id(user_id:str):
    docs = db.collection("pokemon").where(filter=FieldFilter("owner_id","==",user_id)).get()
    return docs

def add_pokemon_to_user_collection(user_id:str,data):
    doc_ref = db.collection('pokemon').document()
    id = data["id"]
    imageUrl = data["imageUrl"]
    name=data["name"]
    type=data["type"]
    owner_id=user_id

    pokemon_data = {
        "id":id,
        "imageUrl":imageUrl,
        "name":name,
        "type":type,
        "owner_id":owner_id
    }
    doc_ref.set(pokemon_data)

    return {
        "message":f"Pokemon captured successfully",
        "id":f"{doc_ref.id}",
        "data":pokemon_data,
        "status":200
    }
def remove_pokemon_from_user_collection(user_id:str,pokemon_id:int):
    snaps = (
    db.collection('pokemon')
    .where('id', '==', pokemon_id)
    .where('owner_id', '==', user_id)
    .limit(1)
    .stream()
    )

    snap = next(snaps, None)
    if not snap or not snap.exists:
        return {"error": "No matching Pokémon found"}

    snap.reference.delete()
    return {"message": "Pokemon released successfully"}
