# built-in modules
import os
from stat import S_IREAD, S_IWRITE


class File:
    """ Set of methods to perform file operations """

    def __init__(self, path):
        """
        :param path: filepath of the file to work with
        """

        self.path = path
        self.crypto_extension = '.ezcrypto'  # default extension for files encrypted by EasyCrypto

    def hide(self) -> None:
        """ Hides a file in the Explorer view """
        os.system(f"attrib +h {self.path}")

    def show(self) -> None:
        """ Shows (unhides) a hidden file in the Explorer view """
        os.system(f"attrib -h {self.path}")

    def readonly(self) -> None:
        """ Sets a file mode to read-only """
        os.chmod(self.path, S_IREAD)

    def writable(self) -> None:
        """ Sets a file mode to read and write """
        os.chmod(self.path, S_IWRITE)

    def lock(self) -> None:
        """ Locks a file (hidden + read-only) """
        self.hide()
        self.readonly()

    def unlock(self) -> None:
        """ Unlocks a file (visible + readable and writable) """
        self.show()
        self.writable()


class CryptUtils:
    """ Set of class/static methods used in both encryption and decryption algorithms """

    def rename_file_correctly(self, path: str, to_encrypt: bool) -> str | None:
        """
        Renames a file correctly, avoiding naming conflicts.

        :param path: original path of the file to rename
        :param to_encrypt: specifies if the file is being encrypted or decrypted
        :return: new file name
         """

        if to_encrypt:

            name = path + self.extension  # adds the default easycrypto extension at the end of the file name
            def_name = avoid_same_file_name(name, cls.extension)

            os.rename(path, def_name)
            return def_name

        else:

            if path[path.rfind('.')::] == cls.extension:  # removes .ezcrypto extension if present
                name = path[:path.rfind('.'):]  # name without .ezcrypto extension

                if name.rfind('.') == -1:  # in case the new name has no extension
                    new_extension = ''
                else:
                    new_extension = name[name.rfind('.')::]

                def_name = cls.avoid_same_file_name(name, new_extension)

                os.rename(path, def_name)
                return def_name

            return None

    @classmethod
    def avoid_same_file_name(cls, name: str, extension: str) -> str:
        """ Keeps generating a new filename until there are no name conflicts, then returns it """

        index = 2
        while os.path.exists(name):
            if index == 2:
                copy = ' - (2)'

                if extension == '':  # in case file has no extension
                    name += copy
                else:
                    name = name[:name.rfind('.'):] + copy + extension

            else:
                place = name.rfind(' - (')
                name = name[:place:] + ' - (' + str(index) + ')' + extension

            index += 1

        return name
