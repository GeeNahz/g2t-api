import os
from typing import List, Union
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore
# from firebase_admin.exceptions import FirebaseError


load_dotenv()

__config = {
    "type": "service_account",
    "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.environ.get('CLIENT_ID'),
    "auth_uri": os.environ.get('AUTH_URI'),
    "token_uri": os.environ.get('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL'),
}

__cred = credentials.Certificate(__config)
firebase_admin.initialize_app(
    credential=__cred
)

class Manager:
    __db = None

    def __init__(self) -> None:
        self.__db = firestore.client()


    def validate(self, collection: str, document: str = None) -> bool:
        if not document:
            doc = self.__db.collection(collection).get()
            if len(doc) < 1:
                return False
            else:
                return True
        else:
            if self.__db.collection(collection).document(document).get().exists:
                return True
            else:
                return False



    def create(self, collection: str, data_obj: dict):
        self.__db.collection(collection).add(data_obj)
        return "Success"


    def get_all(self, collection: str) -> Union[List, bool]:
        docs = self.__db.collection(collection).get()
        all_docs = []
        if len(docs) < 1:
            return False
        else:
            for doc in docs:
                doc_obj = {**doc.to_dict(), "id": doc.id}
                all_docs.append(doc_obj)
            return all_docs


    def get_one(self, collection: str, uid: str): # done
        doc_list = []
        is_valid = self.validate(collection=collection, document=uid)
        if is_valid:
            doc = self.__db.collection(collection).document(uid).get()
            doc_obj = {**doc.to_dict(), "id": doc.id}
            doc_list.append(doc_obj)
            return doc_list
        else:
            return False


    def delete(self, collection: str, uid: str = None):
        is_valid = self.validate(collection=collection, document=uid)
        if is_valid:
            self.__db.collection(collection).document(uid).delete()
            return "Success"
        else:
            return False


    def update(self, collection: str, uid: str, data_obj: dict):
        is_valid = self.validate(collection=collection, document=uid)
        if is_valid:
            self.__db.collection(collection).document(uid).update(data_obj)
            return "Success"
        else:
            return False


    def create_comments(self, collection: str, uid: str, comment_obj: dict):
        self.__db.collection(collection).document(uid).update(
            {"comment": firestore.ArrayUnion([comment_obj])})
            
        return "Success"


    def get_comments(self, collection: str, uid: str):
        comments = self.__db.collection(collection).document(uid).collection('comment').get()
        comments_list = []
        if len(comments) < 1:
            return False
        else:
            for comment in comments:
                comment_obj = {**comment.to_dict(), "id": comment.id}
                comments_list.append(comment_obj)
            return comments_list


    def like_unlike(self, collection: str, uid: str, post_id: str):
        likes = self.__db.collection(collection).document(post_id).get().to_dict().get('like')
        if isinstance(likes, list):
            if uid in likes:
                self.__db.collection(collection).document(post_id).update(
                            {"like": firestore.ArrayRemove([uid])})
            else:
                self.__db.collection(collection).document(post_id).update(
                            {"like": firestore.ArrayUnion([uid])})
        else:
            self.__db.collection(collection).document(post_id).update(
                        {"like": firestore.ArrayUnion([uid])})
        return "Success"


    def filter_db(self, collection: str, **kwargs):
        items_list = []
        is_valid = self.validate(collection=collection)
        if is_valid:
            for value, key in kwargs.items():
                items_list = []
                docs = self.__db.collection(collection).where(key, "==", value).get()
                for doc in docs:
                    items_list.append(doc.to_dict())
            return items_list
        else:
            return False
