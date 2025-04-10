import hashlib

class hasher:
    def __init__(self, file_path):
        self.file_path = file_path

    def hash_file(self):  
        with open(self.file_path, "r") as file_object:
            text = file_object.read()

        encoded_text = text.encode()
        hash_object = hashlib.sha256(encoded_text)
        readable_hash = hash_object.hexdigest()
        return readable_hash  