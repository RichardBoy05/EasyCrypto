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
    ctypes.windll.user32.MessageBoxW(0, "Il file '" + name + "' non è cryptato, oppure"
                                                             " la chiave che stai utilizando non è corretta!", "Error!", 16)

def archive_created_alert(name):
    ctypes.windll.user32.MessageBoxW(0, "Archivio '" + name + "' creato con successo!", "Success!", 64)


def archive_extracted_alert(name):
    ctypes.windll.user32.MessageBoxW(0, "Archivio '" + name + "' decompresso con successo!", "Success!", 64)


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


def not_an_archive_alert(extension):
    ctypes.windll.user32.MessageBoxW(0, "L'estensione del file deve corrispondere con '" + extension + "'",
                                     "Error!", 16)
