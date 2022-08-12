import os
import sys
import shutil
import safedata
from storing import File
from logger import Logger
from config import Config
from firebase import Firebase as Fb
from setusernamegui import SetUsernameGui
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

    log = local_setup()

    log.info('Asking username...')
    result = SetUsernameGui().get_username()

    if result is None or result[1] is None:
        shutdown(log)

    win, username = result

    log.info(f'Username successfully set: {username}')

    configuration(username, log)
    generate_keys(log)
    upload_public_key(win, username, log)


def local_setup():
    if os.path.exists(PATH):
        shutil.rmtree(PATH)

    os.mkdir(PATH)
    os.mkdir(LOGS_PATH)

    log = Logger(__name__).setup()

    log.info('Setup initialized!')
    log.info(f'Directory created: {PATH}')
    log.info(f'Directory created: {LOGS_PATH}')

    os.mkdir(CRYPT_PATH)
    log.info(f'Directory created: {CRYPT_PATH}')
    os.system("attrib +h " + CRYPT_PATH)
    log.info(f'Directory hidden: {CRYPT_PATH}')

    open(STORAGE_FILE, 'w')
    log.info(f'File created: {STORAGE_FILE}')
    File(STORAGE_FILE).lock_file()
    log.info(f'File locked: {STORAGE_FILE}')

    open(CONFIG_FILE, 'w')
    log.info(f'File created: {CONFIG_FILE}')

    Config.initialize()
    log.info('Configuration file initialized!')

    return log


def configuration(username, log):
    Config.add_pair(key='Username', value=username)
    log.info(f'New key-value pair added in the configuration file: Username = {username}')
    Config.add_pair(key='TotalEncryptions', value='0')
    log.info(f'New key-value pair added in the configuration file: TotalEncryptions = 0')
    Config.add_pair(key='TotalDecryptions', value='0')
    log.info(f'New key-value pair added in the configuration file: TotalDecryptions = 0')
    Config.add_pair(key='TotalShares', value='0')
    log.info(f'New key-value pair added in the configuration file: TotalShares = 0')
    Config.add_pair(key='TotalTranslations', value='0')
    log.info(f'New key-value pair added in the configuration file: TotalTranslations = 0')

    File(CONFIG_FILE).lock_file()
    log.info('Configuration file locked!')
    log.info('Configuration file closed!')


def generate_keys(log):
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
        encryption_algorithm=serialization.BestAvailableEncryption(safedata.Safe.password)
    )

    with open(CRYPT_PATH + '\\private_key.pem', 'wb') as f:
        f.write(priv_pem)
    File(CRYPT_PATH + '\\private_key.pem').lock_file()
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


def upload_public_key(win, username, log):
    log.info('Connecting to the server...')

    public_key_file = CRYPT_PATH + '\\public_key.pem'

    if not Fb(win).upload('Users/' + username + '.pem', public_key_file):
        log.critical('Public key could not be uploaded to the server...')
        shutdown(log)

    File(public_key_file).lock_file()
    log.info('Public key successfully uploaded to the server!')
    log.info('Setup successfully COMPLETED!')


def shutdown(log):
    log.critical('Deleting environment...')

    if os.path.exists(PATH) and os.path.exists(STORAGE_FILE) and os.path.exists(CONFIG_FILE):
        File(os.path.join(STORAGE_FILE)).unlock_file()
        File(os.path.join(CONFIG_FILE)).unlock_file()

        shutil.rmtree(PATH, ignore_errors=True)

    sys.exit()
