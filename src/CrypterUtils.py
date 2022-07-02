from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from os import rename
from os.path import exists
from KeyCrypter import decrypt_key
from Alerts import not_encrypted_alert, permission_error_alert, general_exception_alert, not_an_archive_alert


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


def renaming_file(path, extension, to_encrypt):  # if to_encrypt is false, then it is a file to decrypt

    if to_encrypt:

        name = path + extension
        def_name = avoid_same_file_name(name, extension)

        rename(path, def_name)

    else:

        if path[path.rfind('.')::] == extension:
            name = path[:path.rfind('.'):]
            new_extension = name[name.rfind('.')::]

            def_name = avoid_same_file_name(name, new_extension)

            rename(path, def_name)


def avoid_same_file_name(name, extension):
    index = 2
    while exists(name):
        if index == 2:
            copy = ' - (2)'
            name = name[:name.rfind('.'):] + copy + name[name.rfind('.')::]
        else:
            place = name.rfind(' - (')
            name = name[:place:] + ' - (' + str(index) + ')' + extension

        index += 1

    return name


def check_archive_extension(point_index, extension, path):
    if point_index == -1:
        not_an_archive_alert(extension)
        return False

    if path[point_index::] != extension:
        not_an_archive_alert(extension)
        return False

    return True
