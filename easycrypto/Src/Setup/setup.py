# external modules

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

# built-in modules
import os
import sys
import shutil
from tkinter import Tk

# app modules
from easycrypto.Src.Setup.setusernamegui import SetUsernameGui
from easycrypto.Src.Crypt.Local.database import Database
from easycrypto.Src.Utils.file_handler import File
from easycrypto.Src.Utils.config import Config
from easycrypto.Src.Utils.logger import Logger
from easycrypto.Src.Utils.safedata import Safe
from easycrypto.Src.Utils.firebase import Firebase as Fb
from easycrypto.Src.Utils.paths import APP, LOGS, CRYPT, CONFIG_FILE, DATABASE, PRIVATE_KEY, PUBLIC_KEY


class Setup:
    """ Sets up the program environment """

    def __init__(self):

        # check
        if os.path.exists(CONFIG_FILE):  # returns if the program is not being run for the first time
            return
        self.log = None

        # local setup
        self.local_setup()

        # username setup
        result = SetUsernameGui().get_username()
        if result is None or result[1] is None:
            self.shutdown()

        win, username = result  # unpacking SetUsernameGUI output: win -> parent window instance, username -> nickname
        self.log.info(f'Username successfully set: {username}') # noqa (suppress warning)

        # configuration
        self.configuration(username)

        # private and public key generation
        self.generate_keys()

        # public key upload to the server
        self.upload_public_key(win, username)

    def local_setup(self) -> None:
        """ Creates the local environement in the APPDATA folder """

        if os.path.exists(APP):
            shutil.rmtree(APP)

        os.mkdir(APP)
        os.mkdir(LOGS)

        self.log = Logger(__name__).setup()  # logger initialization (couldn't be done before due to directories issues)

        self.log.info('Setup initialized!')
        self.log.info(f'Directory created: {APP}')
        self.log.info(f'Directory created: {LOGS}')

        os.mkdir(CRYPT)
        self.log.info(f'Directory created: {CRYPT}')
        File(CRYPT).hide()
        self.log.info(f'Directory hidden: {CRYPT}')

        open(CONFIG_FILE, 'w')
        self.log.info(f'File created: {CONFIG_FILE}')

        Database().create_main_table()
        self.log.info(f'File created: {DATABASE}')
        self.log.info(f'Created new table "encryption" in {DATABASE}')
        self.log.info(f'File locked: {DATABASE}')

        Config.initialize()
        self.log.info('Configuration file initialized!')
        self.log.info('Asking username...')

    def configuration(self, username: str) -> None:
        """ Appends key-value pairs to the config file """

        Config.add_pair(key='Username', value=username)
        self.log.info(f'New key-value pair added in the configuration file: Username = {username}')
        Config.add_pair(key='TotalEncryptions', value='0')
        self.log.info(f'New key-value pair added in the configuration file: TotalEncryptions = 0')
        Config.add_pair(key='TotalDecryptions', value='0')
        self.log.info(f'New key-value pair added in the configuration file: TotalDecryptions = 0')
        Config.add_pair(key='TotalShares', value='0')
        self.log.info(f'New key-value pair added in the configuration file: TotalShares = 0')
        Config.add_pair(key='TotalTranslations', value='0')
        self.log.info(f'New key-value pair added in the configuration file: TotalTranslations = 0')

        File(CONFIG_FILE).lock()
        self.log.info('Configuration file locked!')
        self.log.info('Configuration file closed!')

    def generate_keys(self) -> None:
        """ Generates and writes to file the user's private and public keys """

        # private key
        self.log.info('Generating private key...')
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )

        self.log.info('Private key serialization...')
        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(Safe.get_privkey_password())
        )

        with open(PRIVATE_KEY, 'wb') as f:
            f.write(priv_pem)
        File(PRIVATE_KEY).lock()
        self.log.info('Private key successfully generated!')

        # public key
        self.log.info('Generating public key...')
        public_key = private_key.public_key()

        self.log.info('Public key serialization...')
        pub_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(PUBLIC_KEY, 'wb') as f:
            f.write(pub_pem)
        self.log.info('Public key successfully generated!')

    def upload_public_key(self, win: Tk, username: str) -> None:
        """ Uploads the public key to the EasyCrypto server """

        self.log.info('Connecting to the server...')

        if not Fb(win).upload(f'Users/{username}.pem', PUBLIC_KEY):
            self.log.critical('Public key could not be uploaded to the server...')
            self.shutdown()

        File(PUBLIC_KEY).lock()
        self.log.info('Public key successfully uploaded to the server!')
        self.log.info('Setup successfully COMPLETED!')

    def shutdown(self) -> None:
        """
        Stops the program and removes its environment, which is used when the installation process encounters an error.
        If a file is still open and cannot be deleted, it will remain, but the program already handles this problem
        """

        self.log.critical('Deleting environment...')

        if os.path.exists(APP) and os.path.exists(DATABASE) and os.path.exists(CONFIG_FILE):
            File(os.path.join(DATABASE)).unlock()
            File(os.path.join(CONFIG_FILE)).unlock()

            shutil.rmtree(APP, ignore_errors=True)

        sys.exit()
