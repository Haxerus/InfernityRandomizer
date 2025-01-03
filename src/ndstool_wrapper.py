import subprocess
import shutil
from pathlib import Path

class NdsToolWrapper():
    def __init__(self, rom_path):
        self.rom_path = rom_path

    def extract(self):
        temp_dir = Path("ndstool/temp")
        if not temp_dir.exists():
            temp_dir.mkdir(parents=True)

        args = ["ndstool\\ndstool.exe",
                "-x", self.rom_path,
                "-9", "ndstool\\temp\\arm9.bin",
                "-7", "ndstool\\temp\\arm7.bin",
                "-y9", "ndstool\\temp\\y9.bin",
                "-y7", "ndstool\\temp\\y7.bin",
                "-d", "ndstool\\temp\\data",
                "-y", "ndstool\\temp\\overlay",
                "-t", "ndstool\\temp\\banner.bin",
                "-h", "ndstool\\temp\\header.bin"]
        subprocess.run(args)
    
    def build(self, output_path):
        temp_dir = Path("ndstool/temp")
        if not temp_dir.exists():
            raise RuntimeError("Extracted ROM files are missing")
        
        args = ["ndstool\\ndstool.exe",
                "-c", output_path,
                "-9", "ndstool\\temp\\arm9.bin",
                "-7", "ndstool\\temp\\arm7.bin",
                "-y9", "ndstool\\temp\\y9.bin",
                "-y7", "ndstool\\temp\\y7.bin",
                "-d", "ndstool\\temp\\data",
                "-y", "ndstool\\temp\\overlay",
                "-t", "ndstool\\temp\\banner.bin",
                "-h", "ndstool\\temp\\header.bin"]
        subprocess.run(args)

        if temp_dir.exists() and temp_dir.is_dir():
            shutil.rmtree(temp_dir)