import os
import firebase as fb
import alerts
from stat import S_IWRITE
from setup import CRYPT_PATH
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from safedata import password, obfuscate_name, deobfuscate_name
from cryptography.hazmat.primitives import hashes, serialization


def get_public_key(username):
    storage = fb.connect()
    if storage is None:
        return None

    key_path = os.path.join(CRYPT_PATH, f'{username}_publickey.pem')
    if not fb.download(storage, f'Users/{username}.pem', CRYPT_PATH, f'{username}_publickey.pem'):
        return None

    with open(key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    os.remove(key_path)

    return public_key


def encrypt_file(path):

    key = Fernet.generate_key()
    encrypter = Fernet(key)

    with open(path, 'rb') as file:
        original_content = file.read()

    try:
        encrypted_content = encrypter.encrypt(original_content)
    except Exception as e:
        alerts.general_exception_alert(e)
        return None

    try:
        with open(path, 'wb') as file:
            file.write(encrypted_content)
    except PermissionError as e:
        alerts.permission_error_alert(e)
        return None
    except Exception as e:
        alerts.general_exception_alert(e)
        return None

    return original_content, key


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
    filepath = os.path.join(CRYPT_PATH, 'tempkey.key')

    with open(filepath, 'wb') as file:
        file.write(key)

    storage = fb.connect()

    if storage is None:
        return None

    if not fb.upload(storage, 'Tokens/' + new_filename + '.key', filepath):
        os.remove(filepath)
        return None

    os.remove(filepath)
    return True


def change_name(username, filename, extension):
    new_username = obfuscate_name(username).replace('-', '#')
    new_filename = obfuscate_name(filename).replace('-', '#') + extension
    return f'{new_username}-{new_filename}'


def get_public_token(location, name):
    storage = fb.connect()
    if storage is None:
        return None

    if not fb.download(storage, location, CRYPT_PATH, 'temp -' + name):
        return None

    encrypted_key_file = os.path.join(CRYPT_PATH, 'temp -' + name)

    if not os.path.exists(encrypted_key_file):
        alerts.not_shared_alert()
        return None

    with open(encrypted_key_file, 'rb') as file:
        encrypted_key = file.read()

    os.remove(encrypted_key_file)

    return encrypted_key


def decrypt_key(encrypted_key):
    with open(CRYPT_PATH + "\\private_key.pem", "rb") as key_file:
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
    os.chmod(path, S_IWRITE)

    with open(path, 'rb') as file:
        encrypted_file = file.read()

    decrypter = Fernet(key)

    try:
        decrypted_content = decrypter.decrypt(encrypted_file)
    except InvalidToken:
        alerts.not_encrypted_alert(path[path.rfind('/') + 1::])
        return None
    except Exception as e:
        alerts.general_exception_alert(e)
        return None

    try:
        with open(path, 'wb') as file:
            file.write(decrypted_content)
    except PermissionError as e:
        alerts.permission_error_alert(e)
        return None
    except Exception as e:
        alerts.general_exception_alert(e)
        return None

    return True


def rename_decrypted_file(path, name):
    name_encoded = name.split('-', 1)[1]
    new_name = deobfuscate_name(name_encoded).replace('#', '-')

    os.rename(path, path[:path.rfind('/'):] + '\\' + new_name)


def clear_storage(location):
    storage = fb.connect()

    if storage is None:
        return None

    storage.delete(location, None)

def is_already_encrypted():
    pass
