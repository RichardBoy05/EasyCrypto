"""

This module contains a set of constants, in
order to easily access program file paths

"""

import os

# directories

APP = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPTO = os.path.join(APP, 'crypto')
LOGS = os.path.join(APP, 'logs')

# files

PRIVATE_KEY = os.path.join(CRYPTO, 'private_key.pem')
PUBLIC_KEY = os.path.join(CRYPTO, 'public_key.pem')
DATABASE = os.path.join(CRYPTO, 'storage.db')
DEF_LOG = os.path.join(LOGS, 'logs.log')
SETUP_LOG = os.path.join(LOGS, 'setup.log')
