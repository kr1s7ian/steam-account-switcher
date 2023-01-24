import customtkinter as ck
from functools import partial
import lib
from lib import config


class Gui(ck.CTk):
    def account_button_click(self, account_index):
        lib.kill_steam()
        lib.login_steam(account_index)
        lib.open_steam()

    def create_account_buttons(self):
        for (account_index, account_title) in enumerate(config.get_account_titles()):
            callback = partial(self.account_button_click, account_index)
            self.button = ck.CTkButton(
                self.frame, text=account_title, command=callback)
            self.button.account_index = account_index
            self.button.pack(padx=5, pady=5)

    def __init__(self):
        super().__init__()

        self.title("Steam Account Switcher")
        self.geometry("600x500")
        self.resizable(0, 0)

        self.frame = ck.CTkFrame(self)
        self.frame.pack()

        self.create_account_buttons()

        self.mainloop()
