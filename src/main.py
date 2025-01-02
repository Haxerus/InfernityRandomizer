from kivy.config import Config
Config.set("graphics", "resizable", 0)

from kivy.app import App
from kivy.app import Widget

import os

class YGORandomizer(Widget):
    pass

class RandomizerApp(App):
    def build(self):
        # Set app properties
        self.icon = "res/icon.png"
        self.title = "Infernity Randomizer v0.1"
        return YGORandomizer()

if __name__ == "__main__":
    RandomizerApp().run()