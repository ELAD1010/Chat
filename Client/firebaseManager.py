"""
import firebase_admin
import datetime
from firebase_admin import credentials
from firebase_admin import storage


class Firebase:

    def __init__(self):
        pass

    @staticmethod
    def upload_img_to_firebase(filename, username):
        bucket = storage.bucket()

        blob = bucket.blob(username)
        blob.upload_from_filename(filename)

    @staticmethod
    def retrieve_img_from_firebase(username):

        bucket = storage.bucket()
        blob = bucket.blob(username)
        if blob.exists():
            return blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
        else:
            return 'https://www.booksie.com/files/profiles/22/mr-anonymous.png'

    @staticmethod
    def init_firebase():
        cred = credentials.Certificate('chatapp-5ae13-firebase-adminsdk-kckf2-483f97655b.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'chatapp-5ae13.appspot.com'
        })
        """