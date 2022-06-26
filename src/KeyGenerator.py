from cryptography.fernet import Fernet
from os import getenv, path, mkdir


def generate_key():

    PATH = getenv('APPDATA') + "\\EasyCrypto"

    if path.exists(PATH):
        return  # TODO: remember to add methods to hide the file and to crypt the key string aswell

    mkdir(PATH)

    with open(PATH + '\\cryptKey.key', 'wb') as file:
        file.write(Fernet.generate_key())
