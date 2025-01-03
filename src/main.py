from kivy.config import Config
Config.set("graphics", "resizable", 0)

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.resources import resource_add_path, resource_find

import os, sys
import random
import hashlib
from threading import Thread

from randomizer import Randomizer

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    default_path = StringProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    default_path = StringProperty(None)

class InfernityRandomizer(FloatLayout):
    file_loaded = BooleanProperty(False)

    seed_input = ObjectProperty(None)

    pack_chk = ObjectProperty(None)
    start_chk = ObjectProperty(None)
    sd_chk = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, default_path=self.get_base_path())
        self._popup = Popup(title="Load ROM", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup, default_path=self.get_base_path())
        self._popup = Popup(title="Save ROM", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.rom_path = os.path.join(path, filename[0])
        self.file_loaded = True
        self.dismiss_popup()
    
    def random_seed(self):
        self.seed_input.text = str(int(random.random() * 1e9))
    
    def get_base_path(self):
        # if hasattr(sys, '_MEIPASS'):
        #     return sys._MEIPASS  # PyInstaller temporary directory
        # return os.path.dirname(os.path.abspath(__file__))  # Script directory for normal execution
        return os.getcwd()

    def save(self, path, filename):
        output_path = os.path.join(path, filename)

        t = Thread(target=self.__randomize, args=(self.rom_path, output_path))
        t.run()

        self.dismiss_popup()
    
    def __randomize(self, in_path, out_path):
        settings = {}

        seed_text = self.seed_input.text
        if seed_text == "":
            settings["seed"] = ""
        else:
            settings["seed"] = int(hashlib.sha256(seed_text.encode()).hexdigest(), 16)

        settings["packs"] = self.pack_chk.active
        settings["starter_deck"] = self.start_chk.active
        settings["structure_deck"] = self.sd_chk.active
        
        randomizer = Randomizer(in_path)
        randomizer.randomize_rom(settings, out_path)

class RandomizerApp(App):
    def build(self):
        # Set app properties
        self.icon = "res/icon.png"
        self.title = "Infernity Randomizer v0.1"
        return InfernityRandomizer()

Factory.register('InfernityRandomizer', cls=InfernityRandomizer)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    RandomizerApp().run()