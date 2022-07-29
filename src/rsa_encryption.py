import os
from rsa_utils import Share
from rsa_utils import Translate
from stat import S_IREAD
from logger import Logger
from safedata import Safe


EXTENSION = '.ezcrypto'


def share(path, username):
    print('qui')
    log = Logger(__name__).default()

    public_key = Share.get_public_key(username)

    if public_key is None:
        return False

    pair = Share.encrypt_file(path)
    Share.add_metadata(path, username)

    original_content = pair[0]
    key = pair[1]

    if key is None:
        return False

    new_filename = Share.change_name(EXTENSION)
    new_path = os.path.join(path[:path.rfind('/') + 1:], new_filename)

    encrypted_key = Share.encrypt_key(key, public_key)
    outcome = Share.publish_encrypted_key(encrypted_key, username, path[path.rfind('/') + 1::])

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
    log = Logger(__name__).default()

    metadata = Translate.get_metadata(path)

    if metadata is None:
        return False

    username = metadata[0]
    filename = metadata[1]
    location = f'Tokens/{Safe.obfuscate_name(username)}-{Safe.obfuscate_name(filename)}.key'

    encrypted_key = Translate.get_public_token(location, path[path.rfind('/') + 1::])

    if encrypted_key is None:
        return False

    key = Translate.decrypt_key(encrypted_key)

    if key is None:
        return False

    outcome = Translate.decrypt_file(path, key)

    if outcome is None:
        return False

    filedefname = Translate.rename_decrypted_file(path, filename)
    Translate.clear_storage(location)

    log_message = f"File translated successfully!\nEncrypted file: {path}\nDecrypted file: {filedefname}"
    log.info(log_message + '\n\n----------------------------------------------------------------------------------\n\n')
    return True
