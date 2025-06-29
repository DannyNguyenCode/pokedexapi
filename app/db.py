import os
import firebase_admin
import json
from firebase_admin import credentials
from dotenv import load_dotenv
from firebase_admin import firestore

load_dotenv()
# 🔑 Works for local AND Vercel
if os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON"):
    cert_dict = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON"))
    cred = credentials.Certificate(cert_dict)
else:
    cred = credentials.Certificate(os.getenv("FIRESTORE_PATH_TO_KEY"))


firebase_admin.initialize_app(cred)

db = firestore.client()
