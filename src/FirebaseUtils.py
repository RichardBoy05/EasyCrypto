import pyrebase
from SafeData import firebaseConfig
from Alerts import general_exception_alert
from os.path import join
from os import getenv
from UsernameGui import ask_username

PATH = join(getenv('APPDATA'), 'EasyCrypto')


def connect():
    try:
        firebase = pyrebase.initialize_app(firebaseConfig)
        storage = firebase.storage()
    except Exception as e:
        general_exception_alert(e)
        return None

    return storage


def download(storage, location, localpath, localname):
    storage.child(location).download(localpath, join(localpath, localname))


def upload(storage, location, local_location):
    storage.child(location).put(local_location)


def delete(storage, location):
    storage.delete(location, None)


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
