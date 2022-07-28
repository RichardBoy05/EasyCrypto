import json
import os
import key_crypter as kc
from logger import default_logger
from stat import S_IREAD, S_IWRITE


def store_data(storage, encrypted_content, salt, key):

    record = {encrypted_content.decode('utf-8'): [salt.decode('ISO-8859-1'), kc.encrypt_key(key).decode('utf-8')]}

    unlock_file(storage)
    unfix_json_format(storage)

    with open(storage, 'a') as file:
        file.write(json.dumps(record, indent=4) + '\n')

    fix_json_format(storage)
    lock_file(storage)


def parse_json(content, storage, check):

    unlock_file(storage)

    with open(storage, 'r') as file:
        if file.read() == "":
            lock_file(storage)
            return None

    with open(storage, 'r') as file:
        db = json.load(file)

    dic = db[0]
    for i in db:
        dic |= i

    try:
        output = dic[content]

        if check:
            lock_file(storage)
            return True

        return output, dic

    except KeyError:

        lock_file(storage)

        log = default_logger(__name__)
        log.warning("KeyError", exc_info=True)
        return None


def remove_json_key(storage, dic, content):

    dic.pop(content, lambda: print("La chiave non esiste!"))

    with open(storage, 'r+') as file:
        file.truncate(0)

    if len(dic) == 0:
        lock_file(storage)
        return

    for key, value in dic.items():
        record = {key: value}
        with open(storage, 'a') as file:
            file.write(json.dumps(record, indent=4) + '\n')

    fix_json_format(storage)
    lock_file(storage)


def fix_json_format(path):
    with open(path, 'r') as file:
        content = file.read()

    content = content.replace('}\n', '},\n')
    content = content[:-2:]
    content = '[' + content + ']'

    with open(path, 'w') as file:
        file.write(content)


def unfix_json_format(path):
    with open(path, 'r') as file:
        content = file.read()

    if len(content) == 0 or content[0] != '[':
        return

    content = content.replace('},\n', '}\n')
    content = content[1:-1:]
    content += '\n'

    with open(path, 'w') as file:
        file.write(content)


def lock_file(file):
    os.system("attrib +h " + file)
    os.chmod(file, S_IREAD)


def unlock_file(file):
    os.system("attrib -h " + file)
    os.chmod(file, S_IWRITE)
