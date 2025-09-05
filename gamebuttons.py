from buttons import *

class CloseSettingsButton(Button):
    """A button to close the settings window"""
    def __init__(self, pos: tuple):
        super().__init__("Close", 20, pos, (10, 100), (100, 100, 200))

    def interact(self):
        global settings, draw
        settings = False
        draw = False