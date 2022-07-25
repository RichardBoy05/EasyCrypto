import os

from Setup import PATH
from FirebaseUtils import connect, upload, download
from os.path import join, exists
from os import remove, chmod, rename
from stat import S_IWRITE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from Alerts import general_exception_alert, permission_error_alert, not_encrypted_alert, not_shared_alert
from SafeData import password, obfuscate_name, deobfuscate_name


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


def publish_encrypted_key(key, new_filename):
    filepath = join(PATH, 'tempkey.key')

    with open(filepath, 'wb') as file:
        file.write(key)

    storage = connect()

    if storage is None:
        return None

    upload(storage, 'Tokens/' + new_filename + '.key', filepath)
    remove(filepath)


def change_name(username, filename, extension):
    new_username = obfuscate_name(username).replace('-', '#')
    new_filename = obfuscate_name(filename).replace('-', '#') + extension
    return new_username + '-' + new_filename


def get_public_token(location, name):
    storage = connect()
    if storage is None:
        return None

    download(storage, location, PATH, 'temp -' + name)
    encrypted_key_file = join(PATH, 'temp -' + name)

    if not exists(encrypted_key_file):
        not_shared_alert()
        return None

    with open(encrypted_key_file, 'rb') as file:
        encrypted_key = file.read()

    os.remove(encrypted_key_file)

    return encrypted_key


def decrypt_key(encrypted_key):
    with open(PATH + "\\private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password,
            backend=default_backend()
        )

    key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return key


def decrypt_file(path, key):
    chmod(path, S_IWRITE)

    with open(path, 'rb') as file:
        encrypted_file = file.read()

    decrypter = Fernet(key)

    try:
        decrypted_content = decrypter.decrypt(encrypted_file)
    except InvalidToken:
        not_encrypted_alert(path[path.rfind('/') + 1::])
        return None
    except Exception as e:
        general_exception_alert(e)
        return None

    try:
        with open(path, 'wb') as file:
            file.write(decrypted_content)
    except PermissionError as e:
        permission_error_alert(e)
        return None
    except Exception as e:
        general_exception_alert(e)
        return None

    return True


def rename_decrypted_file(path, name):
    name_encoded = name.split('-', 1)[1]
    new_name = deobfuscate_name(name_encoded).replace('#', '-')

    rename(path, path[:path.rfind('/'):] + '\\' + new_name)


def clear_storage(location):
    storage = connect()

    if storage is None:
        return None

    storage.delete(location, None)
