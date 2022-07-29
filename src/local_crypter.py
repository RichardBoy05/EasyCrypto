import os
import base64
from key_crypter import KeyCrypter
from storing import File, JsonFile
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey
from stat import S_IREAD, S_IWRITE
from logger import Logger
from alerts import already_encrypted_alert, not_encrypted_alert, permission_error_alert, general_exception_alert, \
    invalid_password


PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT_PATH = os.path.join(PATH, 'crypt')
STORAGE = os.path.join(CRYPT_PATH, 'store.json')


def encrypt(path, password, keep_copy):
    log = Logger(__name__).default()

    with open(path, 'rb') as file:
        original_file = file.read()

    is_already_encrypted = JsonFile(STORAGE).parse_json(original_file.decode('ISO-8859-1'), True)
    if is_already_encrypted:
        already_encrypted_alert(path[path.rfind('/') + 1::])
        return False

    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))

    encrypter = Fernet(key)

    try:
        encrypted_content = encrypter.encrypt(original_file)
    except Exception as e:
        general_exception_alert(e)
        log.error("Exception", exc_info=True)
        return False

    JsonFile(STORAGE).store_data(encrypted_content, salt, key)

    try:
        with open(path, 'wb') as file:
            file.write(encrypted_content)
    except PermissionError as e:
        permission_error_alert(e)
        log.warning("PermissionError", exc_info=True)
        return False
    except Exception as e:
        general_exception_alert(e)
        log.error("Exception", exc_info=True)
        return False

    filedefname = renaming_file(path, '.ezcrypto', True)
    os.chmod(os.path.join(path, filedefname), S_IREAD)

    if keep_copy:
        with open(path, "wb") as file:
            file.write(original_file)

    log_message = f"File encrypted successfully!\nOriginal file: {path}\nEncrypted file: {filedefname}"
    log.info(log_message + '\n\n----------------------------------------------------------------------------------\n\n')
    return True


def decrypt(path, password, keep_copy):
    log = Logger(__name__).default()

    os.chmod(path, S_IWRITE)

    with open(path, 'rb') as file:
        file_content = file.read().decode('ISO-8859-1')

    pair = JsonFile(STORAGE).parse_json(file_content, False)

    if pair is None:
        not_encrypted_alert(path[path.rfind('/') + 1::])
        return False

    salt = pair[0][0].encode('ISO-8859-1')
    key = KeyCrypter(pair[0][1].encode('utf-8')).decrypt_key()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    try:
        kdf.verify(password, base64.urlsafe_b64decode(key))
    except InvalidKey:
        invalid_password(path[path.rfind('/') + 1:path.rfind('.'):])
        log.warning("InvalidKey", exc_info=True)
        File(STORAGE).lock_file()
        return False

    # decryption

    with open(path, 'rb') as file:
        original_file = file.read()

    decrypter = Fernet(key)

    try:
        decrypted_content = decrypter.decrypt(original_file)
    except InvalidToken:
        not_encrypted_alert(path[path.rfind('/') + 1::])
        log.warning("InvalidToken", exc_info=True)
        return False
    except Exception as e:
        general_exception_alert(e)
        log.error("Exception", exc_info=True)
        return False

    try:
        with open(path, 'wb') as file:
            file.write(decrypted_content)
    except PermissionError as e:
        permission_error_alert(e)
        log.warning("PermissionError", exc_info=True)
        return False
    except Exception as e:
        general_exception_alert(e)
        log.error("Exception", exc_info=True)
        return False

    filedefname = renaming_file(path, '.ezcrypto', False)
    os.chmod(os.path.join(path, filedefname), S_IWRITE) if filedefname is not None else os.chmod(path, S_IWRITE)

    if keep_copy:
        with open(path, "wb") as file:
            file.write(original_file)
            os.chmod(path, S_IREAD)
    else:
        JsonFile(STORAGE).remove_json_key(pair[1], file_content)

    log_message = f"File decrypted successfully!\nEncrypted file: {path}\nDecrypted file: {filedefname}"
    log.info(log_message + '\n\n----------------------------------------------------------------------------------\n\n')
    return True


def renaming_file(path, extension, to_encrypt):  # if to_encrypt is false, then it is a file to decrypt

    if to_encrypt:

        name = path + extension
        def_name = avoid_same_file_name(name, extension)

        os.rename(path, def_name)
        return def_name

    else:

        if path[path.rfind('.')::] == extension:
            name = path[:path.rfind('.'):]
            new_extension = name[name.rfind('.')::]

            def_name = avoid_same_file_name(name, new_extension)

            os.rename(path, def_name)
            return def_name


def avoid_same_file_name(name, extension):
    index = 2
    while os.path.exists(name):
        if index == 2:
            copy = ' - (2)'
            name = name[:name.rfind('.'):] + copy + name[name.rfind('.')::]
        else:
            place = name.rfind(' - (')
            name = name[:place:] + ' - (' + str(index) + ')' + extension

        index += 1

    return name


def avoid_same_dir_name(name):
    index = 2
    while os.path.exists(name):
        if index == 2:
            copy = ' - (2)'
            name += copy
        else:
            place = name.rfind(' - (')
            name = name[:place:] + ' - (' + str(index) + ')'

        index += 1

    return name
