class File:

    # constructor

    def __init__(self, name, extension, path, is_encrypted, is_internal):

        self.name = name
        self.extension = extension
        self.path = path
        self.is_encrypted = is_encrypted
        self.is_internal = is_internal

    # methods

    def encrypt(self):
        pass

    def decrypt(self):
        pass

    def decrypt_external_file(self):
        pass

    def send(self):
        pass

    def zip(self):
        pass
