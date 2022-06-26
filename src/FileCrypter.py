from os import getenv, rename
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from KeyCrypter import decrypt_key
import ctypes

KEY_PATH = getenv('APPDATA') + '\\EasyCrypto\\cryptoKey.key'
CRYPTO_EXT = '.ezcrypto'


def encrypt(path):

    if is_already_encrypted(path):
        ctypes.windll.user32.MessageBoxW(0, "Questo file è già stato cryptato!", "Error!")
        return

    key = str.encode(str(decrypt_key()))

    crypter = Fernet(key)

    with open(path, 'rb') as file:
        original_file = file.read()

    encrypted_file = crypter.encrypt(original_file)

    with open(path, 'wb') as file_to_encrypt:
        file_to_encrypt.write(encrypted_file)

    rename(path, path + CRYPTO_EXT)

    ctypes.windll.user32.MessageBoxW(0, "File cryptato con successo", "Success!")


def decrypt(path):

    key = str.encode(decrypt_key())

    decrypter = Fernet(key)

    with open(path, 'rb') as file:
        encrypted_file = file.read()

    try:
        decrypted_file = decrypter.decrypt(encrypted_file)
    except InvalidToken:
        ctypes.windll.user32.MessageBoxW(0, "Questo file non è cryptato!", "Error!")
        return

    with open(path, 'wb') as file_to_decrypt:
        file_to_decrypt.write(decrypted_file)

    if path[path.rfind('.')::] == CRYPTO_EXT:
        rename(path, path[:path.rfind('.'):])

    ctypes.windll.user32.MessageBoxW(0, "File decryptato con successo", "Success!")


def decrypt_external_file(path):
    print("decrypt external file")


def share(path):
    print("share")


def is_already_encrypted(path):

    key = str.encode(str(decrypt_key()))

    decrypter = Fernet(key)

    with open(path, 'rb') as file:
        encrypted_file = file.read()

    try:
        decrypter.decrypt(encrypted_file)
    except InvalidToken:
        return False

    return True

