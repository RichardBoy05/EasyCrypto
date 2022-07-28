import os
import sys
import config
import shutil
import firebase as fb
from safedata import password
from storing import lock_file, unlock_file
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT_PATH = os.path.join(PATH, 'crypt')
STORAGE_FILE = os.path.join(CRYPT_PATH, 'store.json')
CONFIG_FILE = os.path.join(PATH, 'config.ini')
LOGS_PATH = os.path.join(PATH, 'logs')


def setup():
    if os.path.exists(CONFIG_FILE):
        return False

    local_setup()

    log.info('Asking username...')
    username = fb.user(None, True)
    log.info(f'Username successfully set: {username}')

    if username is None:
        shutdown()

    configuration(username)
    generate_keys()
    upload_public_key(username)


def local_setup():
    if os.path.exists(PATH):
        shutil.rmtree(PATH)

    os.mkdir(PATH)
    os.mkdir(LOGS_PATH)

    init_logger()

    log.info('Setup initialized!')
    log.info(f'Directory created: {PATH}')
    log.info(f'Directory created: {LOGS_PATH}')

    os.mkdir(CRYPT_PATH)
    log.info(f'Directory created: {CRYPT_PATH}')
    os.system("attrib +h " + CRYPT_PATH)
    log.info(f'Directory hidden: {CRYPT_PATH}')

    open(STORAGE_FILE, 'w')
    log.info(f'File created: {STORAGE_FILE}')
    lock_file(STORAGE_FILE)
    log.info(f'File locked: {STORAGE_FILE}')

    open(CONFIG_FILE, 'w')
    log.info(f'File created: {CONFIG_FILE}')

    config.initialize()
    log.info('Configuration file initialized!')


def configuration(username):
    config.add_pair(key='Username', value=username)
    log.info(f'New key-value pair added in the configuration file: Username = {username}')
    lock_file(CONFIG_FILE)
    log.info('Configuration file locked!')
    log.info('Configuration file closed!')


def generate_keys():
    log.info('Generating private key...')
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

    log.info('Private key serialization...')
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )

    with open(CRYPT_PATH + '\\private_key.pem', 'wb') as f:
        f.write(priv_pem)
    lock_file(CRYPT_PATH + '\\private_key.pem')
    log.info('Private key successfully generated!')

    log.info('Generating public key...')
    public_key = private_key.public_key()

    log.info('Public key serialization...')
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(CRYPT_PATH + '\\public_key.pem', 'wb') as f:
        f.write(pub_pem)
    log.info('Public key successfully generated!')


def upload_public_key(username):
    log.info('Connecting to the server...')
    storage = fb.connect()

    public_key_file = CRYPT_PATH + '\\public_key.pem'

    if not fb.upload(storage, 'Users/' + username + '.pem', public_key_file):
        log.critical('Public key could not be uploaded to the server...')
        shutdown()

    lock_file(public_key_file)
    log.info('Public key successfully uploaded to the server!')
    log.info('Setup successfully COMPLETED!')


def init_logger():
    from logger import setup_logger
    global log
    log = setup_logger(__name__)


def shutdown():
    log.critical('Deleting environment...')

    if os.path.exists(PATH) and os.path.exists(STORAGE_FILE) and os.path.exists(CONFIG_FILE):
        unlock_file(os.path.join(STORAGE_FILE))
        unlock_file(os.path.join(CONFIG_FILE))

        shutil.rmtree(PATH, ignore_errors=True)

    sys.exit()
