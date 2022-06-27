import ctypes


def encrypted_successfully_alert(tuple_length):
    ctypes.windll.user32.MessageBoxW(0, "File cryptato con successo!", "Success!", 64) if tuple_length == 1 else \
        ctypes.windll.user32.MessageBoxW(0, "File cryptati con successo!", "Success!", 64)


def decrypted_successfully_alert(tuple_length):
    ctypes.windll.user32.MessageBoxW(0, "File decryptato con successo!", "Success!", 64) if tuple_length == 1 else \
        ctypes.windll.user32.MessageBoxW(0, "File decryptati con successo!", "Success!", 64)


def already_encrypted_alert(name):
    ctypes.windll.user32.MessageBoxW(0, "Il file '" + name + "' è già stato cryptato!", "Error!", 16)


def not_encrypted_alert(name):
    ctypes.windll.user32.MessageBoxW(0, "Il file '" + name + "' non è cryptato!", "Error!", 16)


def archive_created_alert(name):
    ctypes.windll.user32.MessageBoxW(0, "Archivio '" + name + "' creato con successo!", "Success", 64)


def archive_extracted_alert(name):
    ctypes.windll.user32.MessageBoxW(0, "Archivio '" + name + "' decompresso con successo!", "Success", 64)
