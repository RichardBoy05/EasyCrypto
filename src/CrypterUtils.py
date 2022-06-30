from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from KeyCrypter import decrypt_key
from Notifications import not_encrypted_alert


def get_crypted_data(path, action):  # actions: 1 -> encrypt; 2 -> check; 3 -> decrypt
    # returns: positive number of the action if successfull; otherwise negative

    key = str.encode(str(decrypt_key(None)))

    crypter = Fernet(key)

    with open(path, 'rb') as file:
        original_file = file.read()

    if action == 1:

        encrypted_file = crypter.encrypt(original_file)
        with open(path, 'wb') as file_to_encrypt:
            file_to_encrypt.write(encrypted_file)
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

        if action == 3:
            with open(path, 'wb') as file_to_decrypt:
                file_to_decrypt.write(decrypted_file)

            return 3


def is_already_encrypted(path):
    outcome = get_crypted_data(path, 2)

    return False if outcome == -2 else True
