from pac_data import PacData

class PacWrapper():
    def __init__(self, path):
        self.path = path

        with open(self.path, "rb") as file:
            file_data = file.read()
            self.pac_data = PacData(file_data)

    def repack(self):
        with open(self.path, "wb") as file:
            file.write(self.pac_data.repack_pac())
    
    def get_file_names(self):
        return self.pac_data.get_file_names()

    def get_file_bytes(self):
        return self.pac_data.get_file_bytes()

    def override_file_data(self, data):
        return self.pac_data.override_file_data(data)