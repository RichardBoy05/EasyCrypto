import pyrebase
import os
from SafeData import firebaseConfig
from Alerts import general_exception_alert
from UsernameGui import ask_username

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')


def connect():
    try:
        firebase = pyrebase.initialize_app(firebaseConfig)
        storage = firebase.storage()
    except Exception as e:
        general_exception_alert(e)
        return None

    return storage


def download(storage, location, localpath, localname):
    try:
        storage.child(location).download(localpath, os.path.join(localpath, localname))
    except Exception as e:
        general_exception_alert(e)


def upload(storage, location, local_location):
    try:
        storage.child(location).put(local_location)
    except Exception as e:
        general_exception_alert(e)


def delete(storage, location):
    try:
        storage.delete(location, None)
    except Exception as e:
        general_exception_alert(e)


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
