from cryptography.fernet import Fernet
from os import getenv, path, mkdir, system
from KeyCrypter import encrypt_key


def generate_key():
    PATH = getenv('APPDATA') + "\\EasyCrypto"

    if path.exists(PATH):
        return

    mkdir(PATH)
    key = Fernet.generate_key()
    crypted_key = str.encode(encrypt_key(str(key)))

    with open(PATH + '\\cryptoKey.key', 'wb') as file:
        file.write(crypted_key)

    system("attrib +h " + PATH)
    system("attrib +h " + PATH + '\\cryptoKey.key')
