import os
import sys
import FirebaseUtils as Fb
from SafeData import password
from StoringUtils import lock_file
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')


def setup():
    if os.path.exists(PATH):
        return

    local_setup()
    username = Fb.user(None, True)

    if username is None:
        handle_errors()

    generate_keys()
    upload_public_key(username)


def local_setup():
    os.mkdir(PATH)
    os.system("attrib +h " + PATH)

    local_storage = PATH + '\\store.json'
    open(local_storage, 'w')
    lock_file(local_storage)


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
        f.write(priv_pem)
    lock_file(PATH + '\\private_key.pem')

    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(PATH + '\\public_key.pem', 'wb') as f:
        f.write(pub_pem)


def upload_public_key(username):
    storage = Fb.connect()

    public_key_file = PATH + '\\public_key.pem'

    Fb.upload(storage, 'Users/' + username + '.pem', public_key_file)
    lock_file(public_key_file)


def handle_errors():
    os.remove(PATH)
    sys.exit()
