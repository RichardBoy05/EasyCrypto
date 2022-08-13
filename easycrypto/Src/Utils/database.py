# built-in modules
import sqlite3

# app modules
from easycrypto.Src.Utils.storing import File
from easycrypto.Src.Utils.paths import DATABASE


class Database:
    """ This class provides a set of methods to work with the Sqlite Database """

    def __init__(self):
        """ Estabilishes a connection with the database """

        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def create_main_table(self) -> None:
        """ Creates a table called 'encryptions' in case it does not exist and defines its structure """

        File(DATABASE).unlock_file()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'encryptions' ("
                            "'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                            "'datas' LONGBLOB UNIQUE NOT NULL,"
                            "'salts' VARBINARY NOT NULL,"
                            "'keys' VARBINARY NOT NULL"
                            ")")

        self.conn.commit()
        File(DATABASE).lock_file()

