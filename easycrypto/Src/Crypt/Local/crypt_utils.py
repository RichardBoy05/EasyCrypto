# external modules
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# built-in modules
import base64

# app modules
from easycrypto.Src.Utils.safedata import Safe


class EncryptUtils:
    """ Set of static methods used in the encryption algorithm """

    @staticmethod
    def derive_key(salt: bytes, password: bytes) -> bytes:
        """ Returns a cryptography token derived from salt (bytes) and password (bytes) """

        kdf = PBKDF2HMAC(  # key derivation function
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        return key

    @staticmethod
    def encrypt_db_entry(value: bytes) -> bytes:
        """ Returns the encrypted 'value' parameter, in order to store it safely into the database """

        encrypter = Fernet(Safe.get_database_key())
        return encrypter.encrypt(value)


class DecryptUtils:
    """ Set of static methods used in the decryption algorithm """

    @staticmethod
    def check_password(password: bytes, salt: bytes, key: bytes) -> bool:
        """
        :param password: password entered by the user to decrypt the file
        :param salt: salt value used to derive the encryption key
        :param key: fernet token to encrypt/decrypt the file
        :return: True, if the password is correct (the same as the one used to encrypt the file), else False
        """

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )

        try:
            kdf.verify(password, base64.urlsafe_b64decode(key))
        except InvalidKey:
            return False

        return True

    @staticmethod
    def decrypt_db_entry(value: bytes) -> bytes:
        """ Returns the decrypted 'value' parameter, retrieved from the encrypted database """

        decrypter = Fernet(Safe.get_database_key())
        return decrypter.decrypt(value)
