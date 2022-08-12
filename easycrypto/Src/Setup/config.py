import os.path
import datetime as dt
from storing import File


class Config:
    CONFIG_FILEPATH = os.path.join(os.path.join(os.getenv('APPDATA'), 'EasyCrypto'), 'config.ini')
    SEPARATOR = ' = '

    @classmethod
    def initialize(cls):
        if os.stat(cls.CONFIG_FILEPATH).st_size != 0:
            return

        with open(cls.CONFIG_FILEPATH, 'w') as file:
            file.write('[EasyCrypto Configuration File]')

        cls.__add_date_comment()

    @classmethod
    def add_pair(cls, key, value):
        with open(cls.CONFIG_FILEPATH, 'a') as file:
            file.write('\n' + key + cls.SEPARATOR + value)

        cls.__add_date_comment()

    @classmethod
    def parse_with_key(cls, key, get_value):  # if get value == True: returns the value else: returns the line
        with open(cls.CONFIG_FILEPATH, 'r') as file:
            lines = file.read().splitlines()

        for index, line in enumerate(lines, 1):

            try:
                if line[0] == '[' or line[0] == ';':
                    continue
            except IndexError:
                pass

            pair = line.split(cls.SEPARATOR, 2)
            if pair[0] == key:

                if get_value:
                    return pair[1]
                else:
                    return lines, index

        return None

    @classmethod
    def edit_key_value_pair(cls, key, new_value):

        result = cls.parse_with_key(key, False)

        if result is None:
            return False

        content, line = result
        content[line - 1] = f'{key} = {new_value}'
        content[line] = f'; {dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}'

        File(cls.CONFIG_FILEPATH).unlock_file()
        with open(cls.CONFIG_FILEPATH, 'w') as file:
            file.writelines(f'{i}\n' for i in content)
        File(cls.CONFIG_FILEPATH).lock_file()

        return True

    @classmethod
    def __add_date_comment(cls):
        current_date = dt.datetime.now()
        string_date = current_date.strftime('%d/%m/%Y, %H:%M:%S')

        with open(cls.CONFIG_FILEPATH, 'a') as file:
            file.write('\n; ' + string_date + '\n')

