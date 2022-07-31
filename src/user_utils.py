import os
import string
import winsound as sound
from config import Config
from firebase import Firebase as Fb

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT_PATH = os.path.join(PATH, 'crypt')
USERS_LIST = os.path.join(PATH, 'users_list.txt')


class Username:

    username = None

    @staticmethod
    def get_users_list():
        if not Fb().download('users_list.txt', PATH, USERS_LIST):
            return None
        return Fb().get_storage()

    @classmethod
    def execute(cls, win, entry_var, to_set, background_canva, canva_id):

        if background_canva.itemcget(canva_id, 'text') != 'Nickname valido!':
            sound.PlaySound('SystemHand', sound.SND_ASYNC)
            return

        cls.username = entry_var.get()

        if os.path.exists(os.path.join(CRYPT_PATH, 'firstboot')):
            cls.username = None

        if to_set:
            filepath = USERS_LIST
            with open(filepath, 'a+') as file:

                file.seek(0)
                if len(file.read(1)) > 0:
                    file.write('\n')
                file.seek(0, 2)
                file.write(cls.username)

            if not Fb().upload('users_list.txt', filepath):
                cls.username = None

        win.destroy()

    @classmethod
    def check_username(cls, username, to_set, canva, canva_id):
        if len(username) < 3:
            canva.itemconfig(canva_id, text='Nickname troppo corto!', fill='red')
            return

        if len(username) > 40:
            canva.itemconfig(canva_id, text='Nickname troppo lungo!', fill='red')
            return

        valid_characters = list(string.ascii_letters + string.digits + '-_.() ')

        for i in username:
            if i not in valid_characters:
                canva.itemconfig(canva_id, text='Il carattere ' + i + ' non è utilizzabile!', fill='red')
                return

        filepath = os.path.join(PATH, 'users_list.txt')

        if to_set:
            if not cls.__is_username_unique(filepath, username):
                canva.itemconfig(canva_id, text='Nickname già esistente!', fill='red')
                return
        else:
            if cls.__is_username_unique(filepath, username):
                canva.itemconfig(canva_id, text='Questo utente non esiste!', fill='red')
                return

            current_username = Config.parse_with_key('Username', True)
            if username == current_username:
                canva.itemconfig(canva_id, text='Questo utente sei tu! Non puoi condividere un file con te stesso!',
                                 fill='red')
                return

        canva.itemconfig(canva_id, text='Nickname valido!', fill='green')

    @staticmethod
    def __is_username_unique(filepath, username):
        with open(filepath, 'r') as file:
            lines = file.read().splitlines()

        for line in lines:
            if line == username:
                return False

        return True
