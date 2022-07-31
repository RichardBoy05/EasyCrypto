import os.path
import datetime as dt


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
    def parse_with_key(cls, key):
        with open(cls.CONFIG_FILEPATH, 'r') as file:
            lines = file.read().splitlines()

        for line in lines:

            try:
                if line[0] == '[' or line[0] == ';':
                    continue
            except IndexError:
                pass

            pair = line.split(cls.SEPARATOR, 2)
            if pair[0] == key:
                return pair[1]

        return None

    @classmethod
    def __add_date_comment(cls):
        current_date = dt.datetime.now()
        string_date = current_date.strftime('%d/%m/%Y, %H:%M:%S')

        with open(cls.CONFIG_FILEPATH, 'a') as file:
            file.write('\n; ' + string_date + '\n')
