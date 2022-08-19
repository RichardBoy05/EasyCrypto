# external modules
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# built-in modules
import os
import json
import string
import random as rand
from stat import S_IWRITE

# app modules
from easycrypto.Src.Utils.paths import CRYPT
from easycrypto.Src.Utils.logger import Logger
from easycrypto.Src.Utils.safedata import Safe
from easycrypto.Src.Utils import alerts as alt
from easycrypto.Src.Utils.firebase import Firebase as Fb
from easycrypto.Src.Crypt.Local.local_crypter import avoid_same_file_name


class RsaUtils:

    def __init__(self, win):
        self.win = win

    @staticmethod
    def pop_invalid_characters(name):
        valid_characters = list(string.ascii_letters + string.digits + '-_.() ')
        newname = [i if i in valid_characters else '§' for i in name]
        return ''.join(newname)


class Share(RsaUtils):

    def __init__(self, win):
        super().__init__(win)

    def is_already_shared(self, path):
        log = Logger(__name__).default()

        with open(path, 'rb') as file:
            # noinspection PyBroadException
            try:
                content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                log.warning('UnicodeDecodeError', exc_info=True)
                return False
            except Exception:
                log.error('Exception', exc_info=True)
                return False

        if '----[METADATA]--->' in content:
            alt.already_shared_alert(self.win, path[path.rfind('/') + 1::])
            return True
        return False

    def check_duped_filenames(self, location):
        if not Fb(self.win).download(location, CRYPT, 'temp.txt'):
            return None

        if os.path.exists(os.path.join(CRYPT_PATH, 'temp.txt')):
            os.remove(os.path.join(CRYPT_PATH, 'temp.txt'))
            return True

        return False

    def get_public_key(self, username):
        key_path = os.path.join(CRYPT_PATH, f'{username}_publickey.pem')
        if not Fb(self.win).download(f'Users/{username}.pem', CRYPT, f'{username}_publickey.pem'):
            return None

        with open(key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        os.remove(key_path)

        return public_key

    def encrypt_file(self, path):
        log = Logger(__name__).default()

        key = Fernet.generate_key()
        encrypter = Fernet(key)

        with open(path, 'rb') as file:
            original_content = file.read()

        try:
            encrypted_content = encrypter.encrypt(original_content)
        except Exception as e:
            alt.general_exception_alert(self.win, e)
            log.error("Exception", exc_info=True)
            return None

        try:
            with open(path, 'wb') as file:
                file.write(encrypted_content)
        except PermissionError as e:
            alt.permission_error_alert(self.win, e)
            log.warning("PermissionError", exc_info=True)
            return None
        except Exception as e:
            alt.general_exception_alert(self.win, e)
            log.error("Exception", exc_info=True)
            return None

        return original_content, key

    @staticmethod
    def add_metadata(path, username):
        filename = path[path.rfind('/') + 1::]
        metadata = f'----[METADATA]--->{{"Username": "{Safe.obfuscate_metadata(username)}", "Filename": "{Safe.obfuscate_metadata(filename)}"}}'

        with open(path, 'rb') as file:
            content = file.read().decode('utf-8')

        with open(path, 'ab') as file:
            file.write((content + metadata).encode('utf-8'))

    @staticmethod
    def change_name(extension):
        return ''.join(rand.choice(string.ascii_letters) for _ in range(15)) + extension

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

    def publish_encrypted_key(self, key, storage_location):
        filepath = os.path.join(CRYPT_PATH, 'tempkey.key')

        with open(filepath, 'wb') as file:
            file.write(key)

        if not Fb(self.win).upload(storage_location, filepath):
            os.remove(filepath)
            return None

        os.remove(filepath)
        return True


class Translate(RsaUtils):

    def __init__(self, win):
        super().__init__(win)

    def get_metadata(self, path):
        log = Logger(__name__).default()

        with open(path, 'rb') as file:
            try:
                content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                log.warning('UnicodeDecodeError', exc_info=True)
                alt.not_shared_alert(self.win)
                return None

        try:
            metadata = content.split('----[METADATA]--->', 1)[1]
        except IndexError:
            log.warning("IndexError", exc_info=True)
            alt.not_shared_alert(self.win)
            return None

        dictionary = json.loads(metadata)

        try:
            username = Safe.obfuscate_metadata(dictionary['Username'])
            filename = Safe.obfuscate_metadata(dictionary['Filename'])
        except KeyError:
            alt.metadata_error_alert(self.win)
            log.error('KeyError', exc_info=True)
            return None

        return username, filename

    def get_public_token(self, location, name):
        if not Fb(self.win).download(location, CRYPT_PATH, 'temp - ' + name):
            return None

        encrypted_key_file = os.path.join(CRYPT_PATH, 'temp - ' + name)

        if not os.path.exists(encrypted_key_file):
            alt.not_shared_alert(self.win)
            return None

        with open(encrypted_key_file, 'rb') as file:
            encrypted_key = file.read()

        os.remove(encrypted_key_file)

        return encrypted_key

    def decrypt_key(self, encrypted_key):
        log = Logger(__name__).default()

        with open(CRYPT_PATH + "\\private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=Safe.get_privkey_password(),
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
            alt.not_shared_alert(self.win)
            return None

        return key

    def decrypt_file(self, path, key):
        log = Logger(__name__).default()

        os.chmod(path, S_IWRITE)

        with open(path, 'rb') as file:
            encrypted_file = file.read()

        decrypter = Fernet(key)

        try:
            decrypted_content = decrypter.decrypt(encrypted_file)
        except InvalidToken:
            alt.not_encrypted_alert(self.win, path[path.rfind('/') + 1::])
            log.warning("InvalidToken", exc_info=True)
            return None
        except Exception as e:
            alt.general_exception_alert(self.win, e)
            log.error("Exception", exc_info=True)
            return None

        try:
            with open(path, 'wb') as file:
                file.write(decrypted_content)
        except PermissionError as e:
            alt.permission_error_alert(self.win, e)
            log.warning("PermissionError", exc_info=True)
            return None
        except Exception as e:
            alt.general_exception_alert(self.win, e)
            log.error("Exception", exc_info=True)
            return None

        return True

    @staticmethod
    def rename_decrypted_file(path, name):
        def_path = os.path.join(path[:path.rfind('/') + 1:], name)
        defname = avoid_same_file_name(def_path, name[name.rfind('.')::])

        os.rename(path, defname)
        return defname

    def clear_storage(self, location):
        Fb(self.win).delete(location)
