import os
import rsa_utils as rsa
from stat import S_IREAD
from logger import default_logger
from safedata import obfuscate_name

EXTENSION = '.ezcrypto'


def share(path, username):
    log = default_logger(__name__)

    public_key = rsa.get_public_key(username)

    if public_key is None:
        return False

    pair = rsa.encrypt_file(path)
    rsa.add_metadata(path, username)

    original_content = pair[0]
    key = pair[1]

    if key is None:
        return False

    new_filename = rsa.change_name(EXTENSION)
    new_path = os.path.join(path[:path.rfind('/') + 1:], new_filename)

    encrypted_key = rsa.encrypt_key(key, public_key)
    outcome = rsa.publish_encrypted_key(encrypted_key, username, path[path.rfind('/') + 1::])

    if outcome is None:
        return False

    os.rename(path, new_path)
    os.chmod(new_path, S_IREAD)

    with open(path, 'wb') as file:
        file.write(original_content)

    log_message = f"File shared successfully!\nOriginal file: {path}\nEncrypted file: {new_filename}\nReceiver: {username}"
    log.info(log_message + '\n\n----------------------------------------------------------------------------------\n\n')
    return True


def translate(path):
    log = default_logger(__name__)

    metadata = rsa.get_metadata(path)

    if metadata is None:
        return False

    username = metadata[0]
    filename = metadata[1]
    location = f'Tokens/{obfuscate_name(username)}-{obfuscate_name(filename)}.key'

    encrypted_key = rsa.get_public_token(location, path[path.rfind('/') + 1::])

    if encrypted_key is None:
        return False

    key = rsa.decrypt_key(encrypted_key)
    outcome = rsa.decrypt_file(path, key)

    if outcome is None:
        return False

    filedefname = rsa.rename_decrypted_file(path, filename)
    rsa.clear_storage(location)

    log_message = f"File translated successfully!\nEncrypted file: {path}\nDecrypted file: {filedefname}"
    log.info(log_message + '\n\n----------------------------------------------------------------------------------\n\n')
    return True
