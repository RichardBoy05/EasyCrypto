import os
import sys
import shutil
import pyrebase
from storing import unlock_file
from usernamegui import ask_username
from safedata import firebaseConfig
from alerts import connection_error_alert

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT_PATH = os.path.join(PATH, 'crypt')


def connect():
    try:
        firebase = pyrebase.initialize_app(firebaseConfig)
        storage = firebase.storage()
    except Exception as e:
        connection_error_alert(e)
        return None

    return storage


def download(storage, location, localpath, localname):
    try:
        storage.child(location).download(localpath, os.path.join(localpath, localname))
        return True
    except Exception as e:
        connection_error_alert(e)
        return False


def upload(storage, location, local_location):
    try:
        storage.child(location).put(local_location)
        return True
    except Exception as e:
        connection_error_alert(e)
        return False


def delete(storage, location):
    try:
        storage.delete(location, None)
        return True
    except Exception as e:
        connection_error_alert(e)
        return False


def user(main_win, to_set):  # if to_set is True -> set username else get username

    username = ask_username(main_win, to_set)

    if username is None:
        return None

    return username


def is_username_unique(filepath, username):
    with open(filepath, 'r') as file:
        lines = file.read().splitlines()

    for line in lines:
        if line == username:
            return False

    return True

