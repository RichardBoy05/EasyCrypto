from os import getenv, remove, listdir
from os.path import isfile, join
from CrypterUtils import get_crypted_data, is_already_encrypted, renaming_file, check_archive_extension
from Alerts import already_encrypted_alert, invalid_archive_alert
from ZipPassword import password as zip_password
from tkinter.filedialog import asksaveasfilename, askdirectory
import pyzipper
from pyzipper import BadZipfile

KEY_PATH = getenv('APPDATA') + '\\EasyCrypto\\cryptoKey.key'
CRYPTO_EXT = '.ezcrypto'
CRYPTO_ARCHIVE_EXT = '.ezcryptozip'


def encrypt(path, bypass_alert):

    if is_already_encrypted(path):
        if not bypass_alert:
            already_encrypted_alert(path[path.rfind('/') + 1::])
        return False

    outcome = get_crypted_data(path, None, 1)

    if outcome == 1:
        renaming_file(path, CRYPTO_EXT, True)

        return True

    return False


def decrypt(path):
    outcome = get_crypted_data(path, None, 3)

    if outcome == 3:
        renaming_file(path, CRYPTO_EXT, False)
        return True

    return False


def decrypt_with_external_key(key_path, file_path):
    outcome = get_crypted_data(file_path, key_path, 3)

    if outcome == 3:
        renaming_file(file_path, CRYPTO_EXT, False)
        return True

    return False


def decrypt_external_file(path):

    if not check_archive_extension(path.rfind('.'), CRYPTO_ARCHIVE_EXT, path):
        return False

    directory = askdirectory(title="Seleziona la cartella dove salvare i file decryptati...")

    if not directory:
        return False

    try:
        with pyzipper.AESZipFile(path) as zf:
            zf.extractall(directory, None, zip_password)
    except BadZipfile:
        invalid_archive_alert()
        return False

    files_and_folders = listdir(directory)
    for i in files_and_folders:
        file = join(directory, i)
        if isfile(file) and file[file.rfind('.')::] == CRYPTO_EXT:
            outcome = decrypt_with_external_key(directory + '/ezcrypto', file)
            if not outcome:
                return False

    remove(directory + '/ezcrypto')

    return True


def share(path):
    filetypes = [('Archivio EasyCrypto', '*' + CRYPTO_ARCHIVE_EXT)]
    file2save = asksaveasfilename(title='Scegli dove salvare l\'archivio cryptato...', filetypes=filetypes,
                                  defaultextension=filetypes)

    if not file2save:
        return False, file2save

    if not file2save[file2save.rfind('.')::] == CRYPTO_ARCHIVE_EXT:
        file2save += CRYPTO_ARCHIVE_EXT

    outcome = []

    for i in path:
        outcome.append(encrypt(i, True))

    with pyzipper.AESZipFile(file2save,
                             'w',
                             compression=pyzipper.ZIP_LZMA,
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(zip_password)
        zf.write(KEY_PATH, 'ezcrypto')

        index = 0

        for i in path:

            if outcome[index]:
                alias = i[i.rfind('/') + 1::] + CRYPTO_EXT
                zf.write(i + CRYPTO_EXT, alias)
                decrypt(i + CRYPTO_EXT)
            else:
                alias = i[i.rfind('/') + 1::]
                zf.write(i, alias)
                decrypt(i)

            index += 1

    return True, file2save
