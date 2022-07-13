from os import getenv, mkdir, path, system, chmod
from stat import S_IREAD


def setup():
    PATH = getenv('APPDATA') + "\\EasyCrypto"

    if path.exists(PATH):
        return

    mkdir(PATH)
    system("attrib +h " + PATH)

    open(PATH + '\\store.json', 'w')
    system("attrib +h " + PATH + '\\store.json')
    chmod(PATH + '\\store.json', S_IREAD)
