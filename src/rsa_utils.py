import os
import json
import alerts
import random as rand
from safedata import Safe
from stat import S_IWRITE
from logger import Logger
from setup import CRYPT_PATH
from string import ascii_letters
from firebase import Firebase as Fb
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from local_crypter import avoid_same_file_name
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization


class Share:

    @staticmethod
    def get_public_key(username):
        key_path = os.path.join(CRYPT_PATH, f'{username}_publickey.pem')
        if not Fb().download(f'Users/{username}.pem', CRYPT_PATH, f'{username}_publickey.pem'):
            return None

        with open(key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        os.remove(key_path)

        return public_key

    @staticmethod
    def encrypt_file(path):
        log = Logger(__name__).default()

        key = Fernet.generate_key()
        encrypter = Fernet(key)

        with open(path, 'rb') as file:
            original_content = file.read()

        try:
            encrypted_content = encrypter.encrypt(original_content)
        except Exception as e:
            alerts.general_exception_alert(e)
            log.error("Exception", exc_info=True)
            return None

        try:
            with open(path, 'wb') as file:
                file.write(encrypted_content)
        except PermissionError as e:
            alerts.permission_error_alert(e)
            log.warning("PermissionError", exc_info=True)
            return None
        except Exception as e:
            alerts.general_exception_alert(e)
            log.error("Exception", exc_info=True)
            return None

        return original_content, key

    @staticmethod
    def add_metadata(path, username):
        filename = path[path.rfind('/') + 1::]
        metadata = f'----[METADATA]--->{{"Username": "{username}", "Filename": "{filename}"}}'

        with open(path, 'rb') as file:
            content = file.read().decode('utf-8')

        with open(path, 'ab') as file:
            file.write((content + metadata).encode('utf-8'))

    @staticmethod
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

    @staticmethod
    def change_name(extension):
        return ''.join(rand.choice(ascii_letters) for _ in range(15)) + extension

    @staticmethod
    def publish_encrypted_key(key, username, original_name):
        filepath = os.path.join(CRYPT_PATH, 'tempkey.key')

        with open(filepath, 'wb') as file:
            file.write(key)

        if not Fb().upload(f'Tokens/{Safe.obfuscate_name(username)}-{Safe.obfuscate_name(original_name)}.key',
                           filepath):
            os.remove(filepath)
            return None

        os.remove(filepath)
        return True

    @staticmethod
    def is_already_encrypted():
        pass


class Translate:

    @staticmethod
    def get_metadata(path):
        log = Logger(__name__).default()

        with open(path, 'rb') as file:
            content = file.read().decode('utf-8')
        try:
            metadata = content.split('----[METADATA]--->', 1)[1]
        except IndexError:
            log.warning("IndexError", exc_info=True)
            alerts.not_shared_alert()
            return None

        dictionary = json.loads(metadata)

        try:
            username = dictionary['Username']
            filename = dictionary['Filename']
        except KeyError:
            alerts.metadata_error_alert()
            log.error('KeyError', exc_info=True)
            return None

        return username, filename

    @staticmethod
    def get_public_token(location, name):
        if not Fb().download(location, CRYPT_PATH, 'temp - ' + name):
            return None

        encrypted_key_file = os.path.join(CRYPT_PATH, 'temp - ' + name)

        if not os.path.exists(encrypted_key_file):
            alerts.not_shared_alert()
            return None

        with open(encrypted_key_file, 'rb') as file:
            encrypted_key = file.read()

        os.remove(encrypted_key_file)

        return encrypted_key

    @staticmethod
    def decrypt_key(encrypted_key):
        log = Logger(__name__).default()

        with open(CRYPT_PATH + "\\private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=Safe.password,
                backend=default_backend()
            )

        try:
            key = private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except ValueError:
            log.warning("ValueError", exc_info=True)
            alerts.not_shared_alert()
            return None

        return key

    @staticmethod
    def decrypt_file(path, key):
        log = Logger(__name__).default()

        os.chmod(path, S_IWRITE)

        with open(path, 'rb') as file:
            encrypted_file = file.read()

        decrypter = Fernet(key)

        try:
            decrypted_content = decrypter.decrypt(encrypted_file)
        except InvalidToken:
            alerts.not_encrypted_alert(path[path.rfind('/') + 1::])
            log.warning("InvalidToken", exc_info=True)
            return None
        except Exception as e:
            alerts.general_exception_alert(e)
            log.error("Exception", exc_info=True)
            return None

        try:
            with open(path, 'wb') as file:
                file.write(decrypted_content)
        except PermissionError as e:
            alerts.permission_error_alert(e)
            log.warning("PermissionError", exc_info=True)
            return None
        except Exception as e:
            alerts.general_exception_alert(e)
            log.error("Exception", exc_info=True)
            return None

        return True

    @staticmethod
    def rename_decrypted_file(path, name):
        def_path = os.path.join(path[:path.rfind('/') + 1:], name)
        defname = avoid_same_file_name(def_path, name[name.rfind('.')::])

        os.rename(path, defname)
        return defname

    @staticmethod
    def clear_storage(location):
        Fb().delete(location)
