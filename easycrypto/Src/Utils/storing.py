
# built-in modules
import os
import json
from stat import S_IREAD, S_IWRITE

# app modules
from easycrypto.Src.Utils.logger import Logger
# from key_crypter import KeyCrypter as Kc


class Storage:

    def __init__(self, filepath):
        self.filepath = filepath


class File(Storage):

    def __init__(self, filepath):
        super().__init__(filepath)

    def lock_file(self):
        os.system(f"attrib +h {self.filepath}")
        os.chmod(self.filepath, S_IREAD)

    def unlock_file(self):
        os.system(f"attrib -h {self.filepath}")
        os.chmod(self.filepath, S_IWRITE)


class JsonFile(File):

    def __init__(self, filepath):
        super().__init__(filepath)

    def store_data(self, encrypted_content, salt, key):
        record = {encrypted_content.decode('utf-8'): [salt.decode('ISO-8859-1'), Kc(key).encrypt_key().decode('utf-8')]}

        self.unlock_file()
        self.__unfix_json_format()

        with open(self.filepath, 'a') as file:
            file.write(json.dumps(record, indent=4) + '\n')

        self.__fix_json_format()
        self.lock_file()

    def parse_json(self, content, check):
        self.unlock_file()

        with open(self.filepath, 'r') as file:
            if file.read() == "":
                self.lock_file()
                return None

        with open(self.filepath, 'r') as file:
            db = json.load(file)

        dic = db[0]
        for i in db:
            dic |= i

        try:
            output = dic[content]

            if check:
                self.lock_file()
                return True

            return output, dic

        except KeyError:

            self.lock_file()

            log = Logger(__name__).default()
            log.warning("KeyError", exc_info=True)
            return None

    def remove_json_key(self, dic, content):
        dic.pop(content, lambda: print("La chiave non esiste!"))

        with open(self.filepath, 'r+') as file:
            file.truncate(0)

        if len(dic) == 0:
            self.lock_file()
            return

        for key, value in dic.items():
            record = {key: value}
            with open(self.filepath, 'a') as file:
                file.write(json.dumps(record, indent=4) + '\n')

        self.__fix_json_format()
        self.lock_file()

    def __fix_json_format(self):
        with open(self.filepath, 'r') as file:
            content = file.read()

        content = content.replace('}\n', '},\n')
        content = content[:-2:]
        content = '[' + content + ']'

        with open(self.filepath, 'w') as file:
            file.write(content)

    def __unfix_json_format(self):
        with open(self.filepath, 'r') as file:
            content = file.read()

        if len(content) == 0 or content[0] != '[':
            return

        content = content.replace('},\n', '}\n')
        content = content[1:-1:]
        content += '\n'

        with open(self.filepath, 'w') as file:
            file.write(content)


