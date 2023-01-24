import lib
from lib import config
from gui import Gui

print(config.data["accounts"])
lib.config.save_config()

Gui()
