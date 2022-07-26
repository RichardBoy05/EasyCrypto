import os
import shutil
import sys
import config
import firebase as fb
from safedata import password
from storing import lock_file, unlock_file
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT_PATH = os.path.join(PATH, 'crypt')
STORAGE_FILE = os.path.join(CRYPT_PATH, 'store.json')
CONFIG_FILE = os.path.join(PATH, 'config.ini')


def setup():
    if os.path.exists(PATH):
        return

    local_setup()
    username = fb.user(None, True)

    if username is None:
        handle_errors()

    configuration(username)
    generate_keys()
    upload_public_key(username)


def local_setup():
    os.mkdir(PATH)
    os.mkdir(CRYPT_PATH)
    os.system("attrib +h " + PATH)
    os.system("attrib +h " + CRYPT_PATH)

    open(STORAGE_FILE, 'w')
    lock_file(STORAGE_FILE)

    open(CONFIG_FILE, 'w')
    config.initialize()


def configuration(username):
    config.add_pair(key='Username', value=username)
    lock_file(CONFIG_FILE)


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )

    with open(CRYPT_PATH + '\\private_key.pem', 'wb') as f:
        f.write(priv_pem)
    lock_file(CRYPT_PATH + '\\private_key.pem')

    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(CRYPT_PATH + '\\public_key.pem', 'wb') as f:
        f.write(pub_pem)


def upload_public_key(username):
    storage = fb.connect()

    public_key_file = CRYPT_PATH + '\\public_key.pem'

    fb.upload(storage, 'Users/' + username + '.pem', public_key_file)
    lock_file(public_key_file)


def handle_errors():
    if os.path.exists(PATH):
        unlock_file(os.path.join(CRYPT_PATH, 'store.json'))
        unlock_file(os.path.join(PATH, 'config.ini'))
        shutil.rmtree(PATH)
    sys.exit()
