import struct
from pac_file import PacFile

class PacData():
    def __init__(self, pac_bytes):
        self.pac_bytes = pac_bytes
        self.data_offset = 0
        self.file_structure = dict()

        sectors = self.__divide_sectors(self.pac_bytes)
        file_names = self.__read_file_names(sectors[0])
        pac_files = self.__get_file_structure(sectors[1])
        self.__fill_file_structure(file_names, pac_files)

    def get_file_names(self):
        return self.file_structure.keys()

    def get_file_bytes(self, file_name):
        if file_name in self.file_structure:
            return self.file_structure.get(file_name).get_data()
        return None

    def override_file_data(self, file_name, data):
        if file_name in self.file_structure:
            self.file_structure.get(file_name).set_data(data)
            return True
        return False

    def repack_pac(self):
        new_file_size = 0

        for pac_file in self.file_structure.values():
            pac_file_space = pac_file.get_address() + pac_file.get_file_size()
            if pac_file_space > new_file_size:
                new_file_size = pac_file_space
        
        new_pac_bytes = bytearray(self.pac_bytes[:new_file_size])

        for pac_file in self.file_structure.values():
            start = pac_file.get_address()
            end = pac_file.get_address() + len(pac_file.get_data())
            new_pac_bytes[start:end] = pac_file.get_data()
        
        return bytes(new_pac_bytes)

    def __divide_sectors(self, file_data):
        header = bytes()
        file_names = bytes()

        i = 0
        while i < len(file_data):
            if (file_data[i] & 0xFF) == 0xFF and (file_data[i+1] & 0xFF) == 0xFF:
                i -= i % 16
                header = file_data[:i]
                break
            i += 2
        
        file_names_offset = i
        while i < len(file_data):
            current_line = file_data[i:i+8]
            if int.from_bytes(current_line) == 0:
                file_names = file_data[file_names_offset:i]
                break
            i += 16
        
        while i < len(file_data):
            current_line = file_data[i:i+8]
            if int.from_bytes(current_line) != 0:
                break
            i += 16
        
        self.data_offset = i
        return [header, file_names]


    def __read_file_names(self, header):
        file_data = header

        line_break_bytes = [0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18]

        words = []
        start = 0

        # Get file names
        for i in range(len(file_data)):
            current_byte = file_data[i]

            if current_byte in line_break_bytes:
                word_bytes = file_data[start:i]
                words.append(word_bytes)

                start = i + 2

                i += 1
        
        end = len(file_data) - 1
        while (file_data[end - 3] & 0xFF) == 0x00:
            end -= 1
        words.append(file_data[start:end])

        return [w for w in words if "." in w.decode("latin_1")]

    def __get_file_structure(self, data):
        files = []

        for i in range(8, len(data), 8):
            data_slice =  data[i:i+8]

            address, file_size = struct.unpack("<ii", data_slice)
            if (file_size > 0):
                files.append(PacFile(file_size, self.data_offset + address))
        
        return files


    def __fill_file_structure(self, file_names, all_files):
        if len(file_names) != len(all_files):
            raise RuntimeError("Mismatch between file name count and file count.")
        
        self.file_structure = dict()

        for i in range(len(file_names)):
            name = file_names[i].decode("latin_1")
            file = all_files[i]
            file.set_file_name(name)

            start = file.get_address()
            end = file.get_address() + file.get_file_size()

            file.set_data(self.pac_bytes[start:end])

            self.file_structure[name] = file