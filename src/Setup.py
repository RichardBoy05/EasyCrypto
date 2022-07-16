from os import getenv, mkdir, path, system, remove
from os.path import join
from SafeData import password
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from JSONUtils import lock_file
from FirebaseUtils import connect, upload, user
from sys import exit

PATH = join(getenv('APPDATA'), 'EasyCrypto')


def setup():

    if path.exists(PATH):
        return

    local_setup()
    username = user(None, True)

    if username is None:
        remove(PATH)
        exit()

    generate_keys()
    upload_public_key(username)


def local_setup():
    mkdir(PATH)
    system("attrib +h " + PATH)

    open(PATH + '\\store.json', 'w')
    lock_file(PATH + '\\store.json')


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

    with open(PATH + '\\private_key.pem', 'wb') as f:
        f.write(priv_pem)  # ricordati di proteggerla con un hash o qualche ambaradam strano
    lock_file(PATH + '\\private_key.pem')

    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(PATH + '\\public_key.pem', 'wb') as f:
        f.write(pub_pem)


def upload_public_key(username):

    storage = connect()
    public_key_file = PATH + '\\public_key.pem'

    upload(storage, 'Users/' + username + '.pem', public_key_file)
    lock_file(public_key_file)