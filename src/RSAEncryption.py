from FirebaseUtils import user
from RSAUtils import get_public_key, encrypt_file, encrypt_key, publish_encrypted_key, random_name
from os import chmod, rename
from os.path import join
from stat import S_IREAD


def share(path):

    username = user(False)
    public_key = get_public_key(username)

    key = encrypt_file(path)

    ex_filename = path[path.rfind('/') + 1:path.rfind('.'):].replace('-', '¶')
    new_filename = random_name('.ezcrypto')

    if key is None:
        return

    encrypted_key = encrypt_key(key, public_key)
    publish_encrypted_key(encrypted_key, username, ex_filename, new_filename[:new_filename.rfind('.')])

    rename(path, join(path[:path.rfind('/'):], new_filename))
    chmod(join(path[:path.rfind('/'):], new_filename), S_IREAD)


def translate():
    pass
