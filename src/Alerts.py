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
    ctypes.windll.user32.MessageBoxW(0, "Il file '" + name + "' non è cryptato!", "Error!",
                                     16)


def permission_error_alert(exception):
    ctypes.windll.user32.MessageBoxW(0, "Non hai il permesso di operare su questo file.\n"
                                        "Verifica che non sia aperto in alcun programma e\n"
                                        "e che non sia in modalità solo lettura.\n\n"
                                        "Ulteriori informazioni:\n" + str(exception),
                                     "Error!", 16)


def general_exception_alert(exception):
    ctypes.windll.user32.MessageBoxW(0, "Errore durante l'esecuzione della richiesta.\n\n"
                                        "Ulteriori informazioni:\n" + str(exception),
                                     "Error!", 16)


def empty_box_alert(box):
    ctypes.windll.user32.MessageBoxW(0, "Il campo \"" + box + "\" è vuoto!", "Error!", 16)


def different_passwords_alert():
    ctypes.windll.user32.MessageBoxW(0, "Le due password non corrispondono!", "Error!", 16)


def invalid_password(filename):
    ctypes.windll.user32.MessageBoxW(0, "La password del file '" + filename + "' non è corretta!", "Error!", 16)


def not_shared_alert():
    ctypes.windll.user32.MessageBoxW(0, "Nessuno ha condiviso questo file con te!", "Error!", 16)
