
# built-in modules
import os
import datetime as dt

# app modules
from easycrypto.Src.Utils.storing import File
from easycrypto.Src.Utils.paths import CONFIG_FILE


class Config:
    """ Provides methods to create and edit the configuration file (config.ini)"""

    SEPARATOR = ' = '

    @classmethod
    def initialize(cls) -> None:
        """ Initialize the config file if it hasn't already been """

        if os.stat(CONFIG_FILE).st_size != 0:
            return

        with open(CONFIG_FILE, 'w') as file:
            file.write('[EasyCrypto Configuration File]')

        cls.__add_date_comment()

    @classmethod
    def add_pair(cls, key: str, value: str) -> None:
        """ Appends a key-value pair to the config file """

        with open(CONFIG_FILE, 'a') as file:
            file.write('\n' + key + cls.SEPARATOR + value)

        cls.__add_date_comment()

    @classmethod
    def parse_with_key(cls, key: str, get_value: bool) -> str | tuple[list[str], int] | None:
        """
        Parses the config file with a key

        Returns:
            - None, if the key doesn't exist
            - The value corresponding the key, if the 'get_value' parameter is True
            - All the lines and index of the key line, if the 'get_value' parameter is False
        """

        with open(CONFIG_FILE, 'r') as file:
            lines = file.read().splitlines()

        for index, line in enumerate(lines, 1):
            try:
                if line[0] == '[' or line[0] == ';':  # skips sections and dates lines
                    continue
            except IndexError:  # exception in case line is empty. This error doesn't affect code flow
                pass

            pair = line.split(cls.SEPARATOR, 2)
            if pair[0] == key:

                output = pair[1] if get_value else lines, index
                return output

        return None  # key not found

    @classmethod
    def edit_key_value_pair(cls, key: str, new_value: str) -> bool:
        """
        Changes the value corresponding to the 'key' parameter with the 'new_value' parameter
        Returns True if the value has been changed, False if the key doesn't exist
        """

        result = cls.parse_with_key(key, False)

        if result is None:  # key doesn't exist
            return False

        content, line = result
        content[line - 1] = f'{key} = {new_value}'
        content[line] = f'; {dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}'

        File(CONFIG_FILE).unlock_file()
        with open(CONFIG_FILE, 'w') as file:  # overwrites the file with the new content
            file.writelines(f'{i}\n' for i in content)
        File(CONFIG_FILE).lock_file()

        return True

    @staticmethod
    def __add_date_comment() -> None:
        """ Appends the current time in the format dd/mm/yyyy, hh:mm:ss """
        date = dt.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')

        with open(CONFIG_FILE, 'a') as file:
            file.write('\n; ' + date + '\n')

