import os.path
import datetime as dt

CONFIG_FILEPATH = os.path.join(os.path.join(os.getenv('APPDATA'), 'EasyCrypto'), 'config.ini')
SEPARATOR = ' = '


def initialize():
    if os.stat(CONFIG_FILEPATH).st_size != 0:
        return

    with open(CONFIG_FILEPATH, 'w') as file:
        file.write('[EasyCrypto Configuration File]')

    add_date_comment()


def add_pair(key, value):
    with open(CONFIG_FILEPATH, 'a') as file:
        file.write('\n' + key + SEPARATOR + value)

    add_date_comment()


def parse_with_key(key):
    with open(CONFIG_FILEPATH, 'r') as file:
        lines = file.read().splitlines()

    for line in lines:

        try:
            if line[0] == '[' or line[0] == ';':
                continue
        except IndexError:
            pass

        pair = line.split(SEPARATOR, 2)
        if pair[0] == key:
            return pair[1]

    return None


def add_date_comment():
    current_date = dt.datetime.now()
    string_date = current_date.strftime('%d/%m/%Y, %H:%M:%S')

    with open(CONFIG_FILEPATH, 'a') as file:
        file.write('\n; ' + string_date + '\n')
