import os
import firebase_admin
from firebase_admin import credentials

def initialise_firebase():
    cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json'))
    firebase_admin.initialize_app(cred)
