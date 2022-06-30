from os import getenv, rename, remove, listdir
from os.path import isfile, join
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from KeyCrypter import decrypt_key
from CrypterUtils import get_crypted_data, is_already_encrypted
from Notifications import already_encrypted_alert, not_encrypted_alert, archive_created_alert, archive_extracted_alert
from ZipPassword import password as zip_password
from tkinter.filedialog import asksaveasfilename, askdirectory
import pyzipper

KEY_PATH = getenv('APPDATA') + '\\EasyCrypto\\cryptoKey.key'
CRYPTO_EXT = '.ezcrypto'
CRYPTO_ARCHIVE_EXT = '.ezcryptozip'


def encrypt(path):
    if is_already_encrypted(path):
        already_encrypted_alert(path[path.rfind('/') + 1::])
        return False

    outcome = get_crypted_data(path, 1)

    if outcome == 1:
        rename(path, path + CRYPTO_EXT)
        return True

    return False


def decrypt(path):

    outcome = get_crypted_data(path, 3)

    if outcome == 3:
        if path[path.rfind('.')::] == CRYPTO_EXT:
            rename(path, path[:path.rfind('.'):])
        return True

    return False


def decrypt_with_external_key(key_path, file_path):

    key = str.encode(decrypt_key(key_path))

    decrypter = Fernet(key)

    with open(file_path, 'rb') as file:
        encrypted_file = file.read()

    try:
        decrypted_file = decrypter.decrypt(encrypted_file)
    except InvalidToken:
        not_encrypted_alert(file_path[file_path.rfind('/') + 1::])
        return False

    with open(file_path, 'wb') as file_to_decrypt:
        file_to_decrypt.write(decrypted_file)

    if file_path[file_path.rfind('.')::] == CRYPTO_EXT:
        rename(file_path, file_path[:file_path.rfind('.'):])


def decrypt_external_file(path):
    directory = askdirectory(title="Seleziona la cartella dove salvare i file decryptati...")

    if not directory:
        return

    with pyzipper.AESZipFile(path) as zf:
        zf.extractall(directory, None, zip_password)

    files_and_folders = listdir(directory)
    for i in files_and_folders:
        file = join(directory, i)
        if isfile(file):
            if file[file.rfind('.')::] == CRYPTO_EXT:
                decrypt_with_external_key(directory + '/ezcrypto', file)

    remove(directory + '/ezcrypto')
    archive_extracted_alert(path[path.rfind('/') + 1::])


def share(path):
    filetypes = [('Archivio EasyCrypto', '*' + CRYPTO_ARCHIVE_EXT)]
    file2save = asksaveasfilename(title='Scegli dove salvare l\'archivio cryptato...', filetypes=filetypes,
                                  defaultextension=filetypes)

    if not file2save:
        return

    if not file2save[file2save.rfind('.')::] == CRYPTO_ARCHIVE_EXT:
        file2save += CRYPTO_ARCHIVE_EXT

    for i in path:
        encrypt(i)
    with pyzipper.AESZipFile(file2save,
                             'w',
                             compression=pyzipper.ZIP_LZMA,
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(zip_password)
        zf.write(KEY_PATH, 'ezcrypto')

        for i in path:
            alias = i[i.rfind('/') + 1::] + CRYPTO_EXT
            zf.write(i + CRYPTO_EXT, alias)
            decrypt(i + CRYPTO_EXT)

    archive_created_alert(file2save[file2save.rfind('/') + 1::])

