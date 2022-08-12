from config import Config


class Counter:

    def __init__(self, win, amount, canvaid):
        self.win = win
        self.amount = amount
        self.canvaid = canvaid

    def update(self, key):
        new_value = int(self.amount) + 1
        self.win.nametowidget('.!canvas').itemconfig(self.canvaid, text=str(new_value))
        Config.edit_key_value_pair(key, new_value)

