# external modules

from cryptography.fernet import Fernet

# built-in modules
import os
from tkinter import Tk

# app modules
from easycrypto.Src.Utils.logger import Logger
from easycrypto.Src.Utils import alerts as alt
from easycrypto.Src.Utils.file_handler import File
from easycrypto.Src.Crypt.Local.database import Database
from easycrypto.Src.Crypt.Local.crypt_utils import EncryptUtils, DecryptUtils


class Crypter:
    """ Contains methods for local encryption/decryption with password """

    def __init__(self, path: str, password: bytes, keepcopy: bool, parent: Tk):
        """
        :param path: absolute path of the file to encrypt/decrypt
        :param password: the password used to encrypt/decrypt the file
        :param keepcopy: if True creates a copy of the original file, else doesn't (default False)
        :param parent: instance of the tkinter parent window, needed to display alerts correctly
        """

        self.path = path
        self.password = password
        self.keepcopy = keepcopy
        self.parent = parent
        self.log = Logger(__name__).default()

    def encrypt(self) -> bool:
        """ :return: True (action performed successfully), False (action couldn't be performed) """

        with open(self.path, 'rb') as file:
            original_content = file.read()

        is_already_encrypted = Database().exists_record(original_content, self.parent)

        if is_already_encrypted is None:  # error while parsing the database
            return False
        elif is_already_encrypted:
            alt.already_encrypted_alert(self.parent, self.path[self.path.rfind('/') + 1::])
            return False

        salt = os.urandom(16)
        key = EncryptUtils.derive_key(salt, self.password)

        encrypter = Fernet(key)

        try:
            encrypted_content = encrypter.encrypt(original_content)
        except Exception as e:
            alt.general_exception_alert(self.parent, e)
            self.log.error("Exception", exc_info=True)
            return False

        if not Database().insert_record(encrypted_content, salt, key, self.parent):
            return False

        try:
            with open(self.path, 'wb') as file:
                file.write(encrypted_content)

        except PermissionError as e:
            alt.permission_error_alert(self.parent, e)
            Database().delete_record(encrypted_content, self.parent)
            self.log.warning("PermissionError", exc_info=True)
            return False

        except Exception as e:
            alt.general_exception_alert(self.parent, e)
            Database().delete_record(encrypted_content, self.parent)
            self.log.error("Exception", exc_info=True)
            return False

        def_path = EncryptUtils.rename_file_correctly(self.path, True)
        File(def_path).readonly()

        if self.keepcopy:
            with open(self.path, "wb") as file:
                file.write(original_content)

        self.log.info(f"File encrypted successfully!\n\nOriginal file: {self.path}\nEncrypted file: {def_path}")

        return True

    def decrypt(self) -> bool:
        """ :return: True (action performed successfully), False (action couldn't be performed) """

        File(self.path).writable()

        with open(self.path, 'rb') as file:
            encrypted_content = file.read()

        selection = Database().select_salt_key(encrypted_content, self.parent)

        if not selection or selection is None:
            if selection is None:
                alt.not_encrypted_alert(self.parent, self.path[self.path.rfind('/') + 1::])
            return False

        salt, key = selection

        if not DecryptUtils.check_password(self.password, salt, key):
            alt.invalid_password(self.parent,  self.path[self.path.rfind('/') + 1::])
            return False

        decrypter = Fernet(key)

        try:
            decrypted_content = decrypter.decrypt(encrypted_content)

        except Exception as e:
            alt.general_exception_alert(self.parent, e)
            self.log.error("Exception", exc_info=True)
            return False

        try:
            with open(self.path, 'wb') as file:
                file.write(decrypted_content)

        except PermissionError as e:
            alt.permission_error_alert(self.parent, e)
            self.log.warning("PermissionError", exc_info=True)
            return False

        except Exception as e:
            alt.general_exception_alert(self.parent, e)
            self.log.error("Exception", exc_info=True)
            return False

        def_path = DecryptUtils.rename_file_correctly(self.path, False)
        File(def_path).readonly() if def_path is not None else File(def_path).writable()

        if self.keepcopy:
            if os.path.exists(self.path):
                path = self.path[:self.path.rfind('/') + 1:] + 'encrypted_file.ezcrypto'
            else:
                path = self.path

            with open(path, "wb") as file:
                file.write(encrypted_content)
                File(path).readonly()
        else:
            Database().delete_record(encrypted_content, self.parent)

        self.log.info(f"File decrypted successfully!\n\nEncrypted file: {self.path}\nDecrypted file: {def_path}")

        return True
