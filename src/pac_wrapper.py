from pac_data import PacData

class PacWrapper():
    def __init__(self, path):
        self.path = path

        with open(self.path, "rb") as file:
            file_data = file.read()
            self.pac_data = PacData(file_data)

    def repack(self):
        try:
            with open(self.path, 'wb') as file:
                file.write(self.pac_data.repack_pac())
        except PermissionError:
            print(f"The file '{self.path}' is already open by another process.")
    
    def get_file_names(self):
        return self.pac_data.get_file_names()

    def get_file_bytes(self, file_name):
        return self.pac_data.get_file_bytes(file_name)

    def override_file_data(self, file_name, data):
        return self.pac_data.override_file_data(file_name, data)