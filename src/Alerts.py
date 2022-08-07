from tkinter import messagebox


def encrypted_successfully_alert(win, tuple_length):
    messagebox.showinfo("Success!", "File cryptato con successo!",
                        parent=win) if tuple_length == 1 else messagebox.showinfo(
        "Success!", "File cryptati con successo!", parent=win)


def decrypted_successfully_alert(win, tuple_length):
    messagebox.showinfo("Success!", "File decryptato con successo!", parent=win) if tuple_length == 1 else \
        messagebox.showinfo("Success!", "File decryptati con successo!", parent=win)


def shared_successfully_alert(win, tuple_length):
    messagebox.showinfo("Success!",
                        "Hai ottenuto una copia criptata del tuo file, pronta per essere condivisa!",
                        parent=win) if tuple_length == 1 else \
        messagebox.showinfo("Success!", "Hai ottenuto delle copie criptate dei tuoi file, pronte per essere condivise!",
                            parent=win)


def translated_successfully_alert(win, tuple_length):
    messagebox.showinfo("Success!", "File tradotto con successo!", parent=win) if tuple_length == 1 else \
        messagebox.showinfo("Success!", "File tradotti con successo!", parent=win)


def already_encrypted_alert(win, name):
    messagebox.showerror("Error!", f"Il file '{name}' è già stato cryptato!", parent=win)


def not_encrypted_alert(win, name):
    messagebox.showerror("Error!", f"Il file '{name}' non è cryptato!", parent=win)


def permission_error_alert(win, e):
    messagebox.showerror("Error!", "Non hai il permesso di operare su questo file.\n"
                                   "Verifica che non sia aperto in alcun programma e\n"
                                   "e che non sia in modalità solo lettura.\n\n"
                                   f"Ulteriori informazioni:\n{e}", parent=win)


def general_exception_alert(win, e):
    messagebox.showerror("Error", "Errore durante l'esecuzione della richiesta.\n\n"
                                  f"Ulteriori informazioni:\n{e}", parent=win)


def empty_box_alert(win, box):
    messagebox.showerror("Error!", f"Il campo '{box}' è vuoto!", parent=win)


def different_passwords_alert(win):
    messagebox.showerror("Error!", "Le due password non corrispondono!", parent=win)


def invalid_password(win, filename):
    messagebox.showerror("Error!", f"La password del file {filename} non è corretta!", parent=win)


def not_shared_alert(win):
    messagebox.showerror("Error!", "Nessuno ha condiviso questo file con te!", parent=win)


def connection_error_alert(win, e):
    messagebox.showerror("Error!",
                         f"Impossibile connettersi al database!\nAssicurati di esssere connesso alla rete!\n\nUlteriori informazioni:\n{e}",
                         parent=win)


def metadata_error_alert(win):
    messagebox.showerror("Error!", "Errore nell'analisi dei metadati del file!", parent=win)


def duplicated_share_alert(win, username, filename):
    messagebox.showerror("Error!",
                         f"Attenzione! Qualcuno ha già condiviso con '{username}' un file denominato '{filename}'. Modifica il nome del file per poterlo condividere!",
                         parent=win)


def already_shared_alert(win, filename):
    messagebox.showerror("Error!", f"Hai già condiviso il file '{filename}'!", parent=win)


def issue_reported_alert(win):
    messagebox.showinfo("Success!", "Segnalazione effettuata con successo!\nSarà presto revisionata.", parent=win)


def issue_error_alert(win, response):
    messagebox.showerror("Error!", f"Impossibile segnalare il problema!\n{response}", parent=win)


def issue_connection_error_alert(win, e):
    messagebox.showerror("Error!", f"Errore di connessione! Assicurati di essere connesso alla rete!\n\n{e}",
                         parent=win)


def empty_issue_attachment_alert(win, filename):
    messagebox.showwarning("Warning!", f"L'allegato {filename} non è stato inviato poiché è vuoto!", parent=win)


def missing_title_alert(win):
    messagebox.showerror("Error!", "Titolo mancante!", parent=win)


def missing_labels_alert(win):
    messagebox.showerror("Error!", "Tag mancante!", parent=win)


def missing_text_alert(win):
    messagebox.showerror("Error!", "Testo mancante!", parent=win)


def missing_attachments(win):
    return messagebox.askyesno("Warning", "Non hai selezionato nessun allegato! Sicuro di voler procedere?", parent=win)
