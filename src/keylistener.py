from pynput import keyboard
import lib
import threading


class KeyListener:
    def on_press(self, key):
        if not self.enabled:
            return

        try:
            pressed_index = int(key.char)
        except:
            return
        if pressed_index == 0:
            return

        if pressed_index > len(lib.config.get_accounts()):
            return

        lib.open_steam_in_account(pressed_index-1, True)

    def listen(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def __init__(self):
        self.enabled = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    def stop(self):
        self.enabled = False

    def start(self):
        self.enabled = True
