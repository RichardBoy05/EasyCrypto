import os
import safedata
import pyrebase
from logger import Logger
from alerts import connection_error_alert


class Firebase:

    def __init__(self):
        self.log = Logger(__name__).default()

        try:
            firebase = pyrebase.initialize_app(safedata.Safe.firebaseConfig)
            storage = firebase.storage()
            self.storage = storage
        except Exception as e:
            connection_error_alert(e)
            self.log.error("Exception", exc_info=True)
            self.storage = None

    def get_storage(self):
        return self.storage

    def check_connection(self):
        if self.get_storage() is None:
            return False
        return True

    def upload(self, location, local_location):
        if not self.check_connection():
            return False

        try:
            self.get_storage().child(location).put(local_location)
            return True
        except Exception as e:
            connection_error_alert(e)
            self.log.error("Exception", exc_info=True)
            return False

    def download(self, location, localpath, localname):
        if not self.check_connection():
            return False

        try:
            self.get_storage().child(location).download(localpath, os.path.join(localpath, localname))
            return True

        except Exception as e:
            connection_error_alert(e)
            self.log.error("Exception", exc_info=True)
            return False

    def delete(self, location):
        if not self.check_connection():
            return False

        try:
            self.get_storage().delete(location, None)
            return True
        except Exception as e:
            connection_error_alert(e)
            self.log.error("Exception", exc_info=True)
            return False
