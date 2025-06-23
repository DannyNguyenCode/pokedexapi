import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
from firebase_admin import firestore

load_dotenv()

PATH_TO_SERVICE_ACCOUNT_KEY = os.getenv("FIRESTORE_PATH_TO_KEY")

cred = credentials.Certificate(PATH_TO_SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)

db = firestore.client()
