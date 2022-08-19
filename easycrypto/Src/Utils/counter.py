# built-in modules
from tkinter import Canvas
from typing import Literal

# app modules
from easycrypto.Src.Utils.config import Config


class Counter:
    """

    - Increments by 1 the corresponding counter (passed via parameter) in the MainGUI
    - Changes the corresponding key-value pair in the configuration to the new incremented value

    """

    def __init__(self, canva: Canvas, canva_object: int,
                 key: Literal['TotalEncryptions', 'TotalDecryptions', 'TotalShares', 'TotalTranslations']):

        self.canva = canva
        self.canva_object = canva_object
        self.key = key

    def update(self) -> None:
        """ Executes the update (both in GUI and configuration file) """

        new_value = int(self.canva.itemcget(self.canva_object, 'text')) + 1

        self.canva.itemconfig(self.canva_object, text=str(new_value))
        Config.edit_key_value_pair(self.key, str(new_value))
