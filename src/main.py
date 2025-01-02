from kivy.config import Config
Config.set("graphics", "resizable", 0)

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup

from ndstool.ndstool_wrapper import NdsToolWrapper

import os

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    default_path = StringProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    default_path = StringProperty(None)

class InfernityRandomizer(FloatLayout):
    load_file = ObjectProperty(None)
    save_file = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, default_path=os.getcwd())
        self._popup = Popup(title="Load ROM", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup, default_path=os.getcwd())
        self._popup = Popup(title="Save ROM", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        rom_path = os.path.join(path, filename[0])
        self.nds_tool = NdsToolWrapper(rom_path)
        self.nds_tool.extract()
        self.dismiss_popup()

    def save(self, path, filename):
        print(os.path.join(path, filename))
        self.dismiss_popup()

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
    RandomizerApp().run()