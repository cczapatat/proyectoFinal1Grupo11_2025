import os

import firebase_admin
from firebase_admin import credentials, db


class FirebaseDatabase:
    def __init__(self):
        self.path = os.getenv('FIREBASE_PATH',
                              os.path.join(os.path.dirname(__file__), '../../data_app/firebase-cred.json'))
        self.database = os.getenv('FIREBASE_DATABASE_MISO', '')
        cred = credentials.Certificate(self.path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': self.database,
        })

    def set_data(self, root: str, data: dict) -> bool:
        if self.database != '' and root != '':
            try:
                ref = db.reference(root)
                ref.set(data)

                return True
            except Exception as e:
                print(f"Error setting data in Firebase: {e}")
                return False
