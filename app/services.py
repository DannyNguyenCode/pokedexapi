import bcrypt
from firebase_admin import auth
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