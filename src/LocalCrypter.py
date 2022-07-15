from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey
from os import rename, chmod, urandom, getenv
from stat import S_IREAD, S_IWRITE
from os.path import exists, join
from KeyCrypter import decrypt_key
from Alerts import already_encrypted_alert, not_encrypted_alert, permission_error_alert, general_exception_alert, \
    invalid_password
from JSONUtils import store_data, parse_json, remove_json_key


PATH = join(getenv('APPDATA'), 'EasyCrypto')
STORAGE = PATH + '\\store.json'


def encrypter(path, password, keep_copy):
    with open(path, 'rb') as file:
        original_file = file.read()

    is_already_encrypted = parse_json(original_file.decode('ISO-8859-1'), STORAGE, True)
    if is_already_encrypted:
        already_encrypted_alert(path[path.rfind('/') + 1::])
        return False

    salt = urandom(16)

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
        return False

    store_data(STORAGE, encrypted_content, salt, key)

    try:
        with open(path, 'wb') as file:
            file.write(encrypted_content)
    except PermissionError as e:
        permission_error_alert(e)
        return False
    except Exception as e:
        general_exception_alert(e)
        return False

    filedefname = renaming_file(path, '.ezcrypto', True)
    chmod(join(path, filedefname), S_IREAD)

    if keep_copy:
        with open(path, "wb") as file:
            file.write(original_file)

    return True


def decrypter(path, password, keep_copy):
    chmod(path, S_IWRITE)

    with open(path, 'rb') as file:
        file_content = file.read().decode('ISO-8859-1')

    pair = parse_json(file_content, STORAGE, False)

    if pair is None:
        not_encrypted_alert(path[path.rfind('/') + 1::])
        return False

    salt = pair[0][0].encode('latin1')
    key = decrypt_key(pair[0][1].encode('utf-8'))

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    try:
        kdf.verify(password, base64.urlsafe_b64decode(key))
    except InvalidKey:
        invalid_password()
        return False

    # decryption

    with open(path, 'rb') as file:
        original_file = file.read()

    decrypter = Fernet(key)

    try:
        decrypted_content = decrypter.decrypt(original_file)
    except InvalidToken:
        not_encrypted_alert(path[path.rfind('/') + 1::])
        return False
    except Exception as e:
        general_exception_alert(e)
        return False

    try:
        with open(path, 'wb') as file:
            file.write(decrypted_content)
    except PermissionError as e:
        permission_error_alert(e)
        return False
    except Exception as e:
        general_exception_alert(e)
        return False

    filedefname = renaming_file(path, '.ezcrypto', False)
    chmod(join(path, filedefname), S_IWRITE)

    if keep_copy:
        with open(path, "wb") as file:
            file.write(original_file)
            chmod(path, S_IREAD)
    else:
        remove_json_key(STORAGE, pair[1], file_content)

    return True


def renaming_file(path, extension, to_encrypt):  # if to_encrypt is false, then it is a file to decrypt

    if to_encrypt:

        name = path + extension
        def_name = avoid_same_file_name(name, extension)

        rename(path, def_name)
        return def_name

    else:

        if path[path.rfind('.')::] == extension:
            name = path[:path.rfind('.'):]
            new_extension = name[name.rfind('.')::]

            def_name = avoid_same_file_name(name, new_extension)

            rename(path, def_name)
            return def_name


def avoid_same_file_name(name, extension):
    index = 2
    while exists(name):
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
    while exists(name):
        if index == 2:
            copy = ' - (2)'
            name += copy
        else:
            place = name.rfind(' - (')
            name = name[:place:] + ' - (' + str(index) + ')'

        index += 1

    return name
