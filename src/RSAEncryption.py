from RSAUtils import *
from os import chmod, rename
from stat import S_IREAD

EXTENSION = '.ezcrypto'


def share(path, username):
    public_key = get_public_key(username)

    key = encrypt_file(path)

    ex_filename = path[path.rfind('/') + 1::]
    new_filename = change_name(username, ex_filename, EXTENSION)

    if key is None:
        return

    encrypted_key = encrypt_key(key, public_key)
    publish_encrypted_key(encrypted_key, new_filename[:new_filename.rfind('.')])

    rename(path, path[:path.rfind('/'):] + '\\' + new_filename)
    chmod(path[:path.rfind('/'):] + '/' + new_filename, S_IREAD)


def translate(path):

    name = path[path.rfind('/') + 1:path.rfind('.'):]
    location = 'Tokens/' + name + '.key'

    encrypted_key = get_public_token(location, name)

    if encrypted_key is None:
        return

    key = decrypt_key(encrypted_key)
    outcome = decrypt_file(path, key)

    if outcome is None:
        return

    rename_decrypted_file(path, name)
    clear_storage(location)
