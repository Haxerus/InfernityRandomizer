class PacFile():
    def __init__(self, file_size, address):
        self.file_name = ""
        self.data = bytes()
        self.file_size = file_size
        self.address = address
    
    def set_file_name(self, file_name):
        self.file_name = file_name
    
    def set_data(self, data):
        self.data = data
    
    def get_file_name(self):
        return self.file_name

    def get_data(self):
        return self.data
    
    def get_file_size(self):
        return self.file_size

    def get_address(self):
        return self.address