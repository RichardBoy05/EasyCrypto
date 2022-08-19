# built-in modules
import os.path
import sqlite3
from tkinter import Tk

# app modules
from easycrypto.Src.Utils.logger import Logger
from easycrypto.Src.Utils import alerts as alt
from easycrypto.Src.Utils.paths import DATABASE
from easycrypto.Src.Utils.file_handler import File
from easycrypto.Src.Crypt.Local.crypt_utils import EncryptUtils, DecryptUtils


class Database:
    """ This class provides a set of methods to work with the Sqlite Database """

    def __init__(self):
        """ Estabilishes a connection with the database """

        if os.path.exists(DATABASE):
            File(DATABASE).unlock()

        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()
        self.log = Logger(__name__).default()

    def create_main_table(self) -> None:
        """ Creates a table called 'encryptions' in case it does not exist and defines its structure """

        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'encryptions' ("
                            "'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                            "'datas' VARBINARY UNIQUE NOT NULL,"
                            "'salts' VARBINARY NOT NULL,"
                            "'keys' VARBINARY NOT NULL"
                            ")")

        self.conn.commit()
        File(DATABASE).lock()

    def insert_record(self, data: bytes, salt: bytes, key: bytes, parent: Tk) -> bool:
        """
        Stores encrypted content, salt and keys into the database
        :return: True, if values has been stored successfully, else False
        """

        enc_salt = EncryptUtils.encrypt_db_entry(salt)
        enc_key = EncryptUtils.encrypt_db_entry(key)

        try:
            self.cursor.execute(
                f"INSERT INTO encryptions (datas, salts, keys) VALUES (?, ?, ?)", (data, enc_salt, enc_key))
            self.conn.commit()

        # exceptions handling
        except sqlite3.OperationalError as e:
            self.log.error('sqlite3.OperationalError', exc_info=True)
            alt.corrupted_database(parent, e)
            File(DATABASE).lock()
            return False
        except Exception as ex:
            self.log.error('Exception', exc_info=True)
            alt.corrupted_database(parent, ex)
            File(DATABASE).lock()
            return False

        File(DATABASE).lock()

        return True

    def exists_record(self, data: bytes, parent: Tk) -> bool | None:
        """
        :return: bool -> True if DB contains a record where column 'datas' == data (parameter), else False
        :return: None -> An error occured while parsing the database
        """

        try:
            self.cursor.execute(f"SELECT 1 FROM encryptions WHERE datas = ? LIMIT 1", (data,))

        # exceptions handling
        except sqlite3.OperationalError as e:
            self.log.error('sqlite3.OperationalError', exc_info=True)
            alt.corrupted_database(parent, e)
            File(DATABASE).lock()
            return None
        except Exception as ex:
            self.log.error('Exception', exc_info=True)
            alt.corrupted_database(parent, ex)
            File(DATABASE).lock()
            return None

        File(DATABASE).lock()

        if len(self.cursor.fetchall()) == 0:  # no records found case
            return False

        return True

    def delete_record(self, data: bytes, parent=Tk) -> bool:
        """
        Deletes a record from the database where column 'datas' == data (parameter)
        :return: True, action performed successfully, else False
        """

        try:
            self.cursor.execute(f"DELETE FROM encryptions WHERE datas = ?", (data,))
            self.conn.commit()

        # exceptions handling
        except sqlite3.OperationalError as e:
            self.log.error('sqlite3.OperationalError', exc_info=True)
            alt.corrupted_database(parent, e)
            File(DATABASE).lock()
            return False
        except Exception as ex:
            self.log.error('Exception', exc_info=True)
            alt.corrupted_database(parent, ex)
            File(DATABASE).lock()
            return False

        File(DATABASE).lock()

        return True

    def select_salt_key(self, data: bytes, parent: Tk) -> list[bytes, bytes] | None | bool:
        """
        Parses the database and returns salt and key matching the 'data' parameter value

        :param data: the contents of the encrypted file used to parse the database
        :param parent: instance of the tkinter parent window, needed to display alerts correctly
        :return: corresponding salt and key (bytes), None if not found, False if errors occured
        """

        try:
            self.cursor.execute(f"SELECT salts, keys FROM encryptions WHERE datas = ? LIMIT 1", (data,))

        # exceptions handling
        except sqlite3.OperationalError as e:
            self.log.error('sqlite3.OperationalError', exc_info=True)
            alt.corrupted_database(parent, e)
            File(DATABASE).lock()
            return False
        except Exception as ex:
            self.log.error('Exception', exc_info=True)
            alt.corrupted_database(parent, ex)
            File(DATABASE).lock()
            return False

        File(DATABASE).lock()

        result = self.cursor.fetchall()
        if len(result) == 0:
            return None

        return [DecryptUtils.decrypt_db_entry(i) for i in result[0]]  # decrypts each element of the list and returns

