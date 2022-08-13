"""

This module contains a set of constants, in
order to easily access program file paths

"""

import os
from pathlib import Path

# directories

APP = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT = os.path.join(APP, 'crypto')
LOGS = os.path.join(APP, 'logs')
ROOT = Path.cwd().parent

# files

CONFIG_FILE = os.path.join(APP, 'config.ini')
PRIVATE_KEY = os.path.join(CRYPT, 'private_key.pem')
PUBLIC_KEY = os.path.join(CRYPT, 'public_key.pem')
DATABASE = os.path.join(CRYPT, 'storage.db')
DEF_LOG = os.path.join(LOGS, 'logs.log')
SETUP_LOG = os.path.join(LOGS, 'setup.log')
USERS_LIST = os.path.join(APP, 'users_list.txt')
