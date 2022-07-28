import os
import rsa_utils as rsa
from stat import S_IREAD
from logger import default_logger

EXTENSION = '.ezcrypto'


def share(path, username):
    log = default_logger(__name__)

    public_key = rsa.get_public_key(username)

    if public_key is None:
        return False

    pair = rsa.encrypt_file(path)

    original_content = pair[0]
    key = pair[1]

    if key is None:
        return False

    ex_filename = path[path.rfind('/') + 1::]
    new_filename = rsa.change_name(username, ex_filename, EXTENSION)

    encrypted_key = rsa.encrypt_key(key, public_key)
    outcome = rsa.publish_encrypted_key(encrypted_key, new_filename[:new_filename.rfind('.')])

    if outcome is None:
        return False

    filedefname = path[:path.rfind('/'):] + '\\' + new_filename
    os.rename(path, filedefname)
    os.chmod(filedefname, S_IREAD)

    with open(path, 'wb') as file:
        file.write(original_content)

    log_message = f"File shared successfully!\nOriginal file: {path}\nEncrypted file: {filedefname}\nReceiver: {username}"
    log.info(log_message + '\n\n----------------------------------------------------------------------------------\n\n')
    return True


def translate(path):
    log = default_logger(__name__)

    name = path[path.rfind('/') + 1:path.rfind('.'):]
    location = f'Tokens/{name}.key'

    encrypted_key = rsa.get_public_token(location, name)

    if encrypted_key is None:
        return False

    key = rsa.decrypt_key(encrypted_key)
    outcome = rsa.decrypt_file(path, key)

    if outcome is None:
        return False

    filedefname = rsa.rename_decrypted_file(path, name)
    rsa.clear_storage(location)

    log_message = f"File translated successfully!\nEncrypted file: {path}\nDecrypted file: {filedefname}"
    log.info(log_message + '\n\n----------------------------------------------------------------------------------\n\n')
    return True
