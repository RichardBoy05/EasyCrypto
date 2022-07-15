from Setup import PATH
from FirebaseUtils import connect, upload, download
from os.path import join
from os import remove, rename, chmod
from stat import S_IREAD
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
from Alerts import general_exception_alert, permission_error_alert
from random import choices
from string import ascii_letters, digits


def get_public_key(username):
    storage = connect()
    if storage is None:
        return None

    key_path = join(PATH, username + '_publickey.pem')
    download(storage, 'Users/' + username + '.pem', PATH, key_path)

    with open(key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    remove(key_path)

    return public_key


def encrypt_file(path):
    key = Fernet.generate_key()
    encrypter = Fernet(key)

    with open(path, 'rb') as file:
        original_content = file.read()

    try:
        encrypted_content = encrypter.encrypt(original_content)
    except Exception as e:
        general_exception_alert(e)
        return None

    try:
        with open(path, 'wb') as file:
            file.write(encrypted_content)
    except PermissionError as e:
        permission_error_alert(e)
        return None
    except Exception as e:
        general_exception_alert(e)
        return None

    return key


def encrypt_key(key, public_key):
    encrypted_key = public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key


def publish_encrypted_key(key, username, ex_filename, new_filename):
    filepath = join(PATH, 'tempkey.key')

    with open(filepath, 'wb') as file:
        file.write(key)

    storage = connect()

    if storage is None:
        return None

    upload(storage, 'Tokens/' + username + '-' + new_filename + '-' + ex_filename + '.key', filepath)
    remove(filepath)


def random_name(extension):
    filename = ''.join(choices(ascii_letters + digits, k=10)) + extension
    return filename
