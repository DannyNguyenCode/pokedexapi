import bcrypt
from firebase_admin import auth
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def generate_response(message:str,status:int, **data):
    response = {
        "message": message,
        "status":status,
        "data":data
    }
    return response


def hash_password(password:str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(),salt)
    return hashed_password.decode()

def check_password(password:str, hashed_password:str):
    return bcrypt.checkpw(password.encode(),hashed_password.encode())
    
def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as error:
        return None
    
def generate_jwt(payload, expires_in_minutes=60):
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
    token = jwt.encode(payload,SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token):
    try:
        decoded = jwt.decode(token,SECRET_KEY,algorithm="HS256")
        return decoded    
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None