import os
import rsa_utils as rsa
from stat import S_IREAD

EXTENSION = '.ezcrypto'


def share(path, username):
    public_key = rsa.get_public_key(username)

    key = rsa.encrypt_file(path)

    ex_filename = path[path.rfind('/') + 1::]
    new_filename = rsa.change_name(username, ex_filename, EXTENSION)

    if key is None:
        return

    encrypted_key = rsa.encrypt_key(key, public_key)
    rsa.publish_encrypted_key(encrypted_key, new_filename[:new_filename.rfind('.')])

    os.rename(path, path[:path.rfind('/'):] + '\\' + new_filename)
    os.chmod(path[:path.rfind('/'):] + '/' + new_filename, S_IREAD)


def translate(path):

    name = path[path.rfind('/') + 1:path.rfind('.'):]
    location = 'Tokens/' + name + '.key'

    encrypted_key = rsa.get_public_token(location, name)

    if encrypted_key is None:
        return

    key = rsa.decrypt_key(encrypted_key)
    outcome = rsa.decrypt_file(path, key)

    if outcome is None:
        return

    rsa.rename_decrypted_file(path, name)
    rsa.clear_storage(location)
