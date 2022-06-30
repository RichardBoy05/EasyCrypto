from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from os import rename
from KeyCrypter import decrypt_key
from Alerts import not_encrypted_alert, permission_error_alert, general_exception_alert


def get_crypted_data(path, keypath, action):  # actions: 1 -> encrypt; 2 -> check; 3 -> decrypt
    # returns: positive number of the action if successfull; otherwise negative

    key = str.encode(str(decrypt_key(keypath)))

    crypter = Fernet(key)

    with open(path, 'rb') as file:
        original_file = file.read()

    if action == 1:

        try:
            encrypted_file = crypter.encrypt(original_file)
        except Exception as e:
            general_exception_alert(e)
            return -1

        try:
            with open(path, 'wb') as file_to_encrypt:
                file_to_encrypt.write(encrypted_file)
        except PermissionError as e:
            permission_error_alert()
            return -1
        except Exception as e:
            general_exception_alert(e)
            return -1

        return 1

    else:
        try:
            decrypted_file = crypter.decrypt(original_file)
        except InvalidToken:

            if action == 2:
                return -2
            else:
                not_encrypted_alert(path[path.rfind('/') + 1::])
                return -3

        except Exception as e:

            general_exception_alert(e)
            return -2 if action == 2 else -3

        if action == 3:

            try:
                with open(path, 'wb') as file_to_decrypt:
                    file_to_decrypt.write(decrypted_file)
            except PermissionError as e:
                permission_error_alert(e)
                return -3
            except Exception as e:
                general_exception_alert(e)
                return -3

            return 3


def is_already_encrypted(path):
    outcome = get_crypted_data(path, None, 2)

    return False if outcome == -2 else True


def renaming_after_decryption(path, extension):

    if path[path.rfind('.')::] == extension:
        rename(path, path[:path.rfind('.'):])
