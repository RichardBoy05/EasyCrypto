from os import getenv, rename
from cryptography.fernet import Fernet
import ctypes

KEY_PATH = getenv('APPDATA') + '\\EasyCrypto\\cryptKey.key'
CRYPTO_EXT = '.ezcrypto'


def encrypt(path):

    if path[path.rfind('.')::] == CRYPTO_EXT:
        ctypes.windll.user32.MessageBoxW(0, "Questo file è già stato cryptato!", "Error!")
        return

    with open(KEY_PATH, 'rb') as key_path:
        key = key_path.read()

    crypter = Fernet(key)

    with open(path, 'rb') as file:
        original_file = file.read()

    encrypted_file = crypter.encrypt(original_file)

    with open(path, 'wb') as file_to_encrypt:
        file_to_encrypt.write(encrypted_file)

    rename(path, path + CRYPTO_EXT)

    ctypes.windll.user32.MessageBoxW(0, "File cryptato con successo", "Success!")


def decrypt(path):

    if path[path.rfind('.')::] != CRYPTO_EXT:
        ctypes.windll.user32.MessageBoxW(0, "Questo file non è cryptato!", "Error!")
        return

    with open(KEY_PATH, 'rb') as key_path:
        key = key_path.read()

    decrypter = Fernet(key)

    with open(path, 'rb') as file:
        encrypted_file = file.read()

    decrypted_file = decrypter.decrypt(encrypted_file)

    with open(path, 'wb') as file_to_decrypt:
        file_to_decrypt.write(decrypted_file)

    rename(path, path[:path.rfind('.'):])
    ctypes.windll.user32.MessageBoxW(0, "File decryptato con successo", "Success!")


def decrypt_external_file(path):
    print("decrypt external file")


def share(path):
    print("share")
