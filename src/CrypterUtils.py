from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey
from os import getenv, rename, chmod, system, urandom
from stat import S_IREAD, S_IWRITE
from os.path import exists, join
from KeyCrypter import encrypt_key, decrypt_key
from Alerts import not_encrypted_alert, permission_error_alert, general_exception_alert, not_an_archive_alert
import json

PATH = getenv('APPDATA') + "\\EasyCrypto"


def get_crypted_data(path, keypath, action):  # actions: 1 -> encrypt; 2 -> check; 3 -> decrypt
    # returns: positive number of the action if successfull; otherwise negative

    key = str.encode(str(decrypt_key(keypath)))

    crypter = Fernet(key)

    with open(path, 'rb') as file:
        original_file = file.read()

    if action == 1:

        try:
            encrypted_file = crypter.encrypt(original_file)
        except Exception as e:
            general_exception_alert(e)
            return -1

        try:
            with open(path, 'wb') as file_to_encrypt:
                file_to_encrypt.write(encrypted_file)
        except PermissionError as e:
            permission_error_alert()
            return -1
        except Exception as e:
            general_exception_alert(e)
            return -1

        return 1

    else:
        try:
            decrypted_file = crypter.decrypt(original_file)
        except InvalidToken:

            if action == 2:
                return -2
            else:
                not_encrypted_alert(path[path.rfind('/') + 1::])
                return -3

        except Exception as e:

            general_exception_alert(e)
            return -2 if action == 2 else -3

        if action == 3:

            try:
                with open(path, 'wb') as file_to_decrypt:
                    file_to_decrypt.write(decrypted_file)
            except PermissionError as e:
                permission_error_alert(e)
                return -3
            except Exception as e:
                general_exception_alert(e)
                return -3

            return 3


def is_already_encrypted(path):
    outcome = get_crypted_data(path, None, 2)

    return False if outcome == -2 else True


def encrypter_with_password(path, password, keep_copy):
    salt = urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))

    with open(path, 'rb') as file:
        original_file = file.read()

    encrypter = Fernet(key)
    encrypted_content = encrypter.encrypt(original_file)

    with open(path, 'wb') as file:
        file.write(encrypted_content)

    filedefname = renaming_file(path, '.ezcrypto', True)
    chmod(join(path, filedefname), S_IREAD)

    if keep_copy:
        with open(path, "wb") as file:
            file.write(original_file)

    # storing

    storage = PATH + '\\store.json'
    record = {encrypted_content.decode('utf-8'): [salt.decode('latin1'), encrypt_key(key).decode('utf-8')]}

    system("attrib -h " + storage)
    chmod(storage, S_IWRITE)

    unfix_json_format(storage)

    with open(storage, 'a') as file:
        file.write(json.dumps(record, indent=4) + '\n')

    fix_json_format(storage)

    system("attrib +h " + storage)
    chmod(storage, S_IREAD)


def decrypter_with_password(path, password, keep_copy):
    storage = PATH + '\\store.json'
    chmod(path, S_IWRITE)

    with open(path, 'rb') as file:
        file_content = file.read().decode('utf-8')

    system("attrib -h " + storage)
    chmod(storage, S_IWRITE)

    with open(storage, 'r') as file:
        db = json.load(file)

    pair = parse_json(file_content, db)

    system("attrib +h " + storage)
    chmod(storage, S_IREAD)

    salt = pair[0].encode('latin1')
    key = decrypt_key(pair[1].encode('utf-8'))

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    try:
        kdf.verify(password, base64.urlsafe_b64decode(key))
    except InvalidKey:
        print("Le due password non corrispondono!")
        return False

    # decryption

    with open(path, 'rb') as file:
        original_file = file.read()

    decrypter = Fernet(key)
    decrypted_content = decrypter.decrypt(original_file)

    with open(path, 'wb') as file:
        file.write(decrypted_content)

    filedefname = renaming_file(path, '.ezcrypto', False)
    chmod(join(path, filedefname), S_IWRITE)

    if keep_copy:
        with open(path, "wb") as file:
            file.write(original_file)
            chmod(path, S_IREAD)


def parse_json(content, db):

    dic = db[0]

    for i in db:
        dic |= i

    try:
        return dic[content]
    except KeyError:
        print("La chiave non esiste!")
        return None


def fix_json_format(path):
    with open(path, 'r') as file:
        content = file.read()

    content = content.replace('}', '},')
    content = content[:-2:]
    content = '[' + content + ']'

    with open(path, 'w') as file:
        file.write(content)


def unfix_json_format(path):
    with open(path, 'r') as file:
        content = file.read()

    if len(content) == 0 or content[0] != '[':
        return

    content = content.replace('},', '}')
    content = content[1:-1:]
    content += '\n'

    with open(path, 'w') as file:
        file.write(content)


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


def check_archive_extension(point_index, extension, path):
    if point_index == -1:
        not_an_archive_alert(extension)
        return False

    if path[point_index::] != extension:
        not_an_archive_alert(extension)
        return False

    return True
