import pyrebase
from SafeData import firebaseConfig
from Alerts import general_exception_alert
from os.path import join
from os import system, remove, getenv

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


def user(to_set):  # if True -> set username else get username

    if to_set:
        text = "Inserisci il tuo nome utente: (sostituisci con interfaccia ndr)"
    else:
        text = "Seleziona un utente: (sostituisci con interfaccia ndr)"

    username = input(text)

    storage = connect()
    if storage is None:
        return None

    download(storage, 'users_list.txt', PATH, PATH + '\\users_list.txt')

    if to_set:
        while not is_username_unique(PATH + '\\users_list.txt', username):
            username = input(text)
    else:
        while is_username_unique(PATH + '\\users_list.txt', username):
            username = input(text)

    if to_set:
        with open(PATH + '\\users_list.txt', 'a+') as file:

            file.seek(0)
            if len(file.read(1)) > 0:
                file.write('\n')
            file.seek(0, 2)
            file.write(username)

        upload(storage, 'users_list.txt', PATH + '\\users_list.txt')

    remove(PATH + '\\users_list.txt')

    return username


def is_username_unique(filepath, username):
    with open(filepath, 'r') as file:
        lines = file.read().splitlines()

    for line in lines:
        if line == username:
            return False

    return True
