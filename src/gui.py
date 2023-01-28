import customtkinter as ck
from functools import partial
import os
import lib
from accountbox import AccountBox
from lib import config

ck.set_appearance_mode("dark")
ck.set_default_color_theme('Assets/Theme.json')


class Gui(ck.CTk):

    def close_on_switch(self):
        config.set_close_on_switch(not config.get_close_on_switch())
        config.save()

    def clear_accounts_button_press(self):
        config.clear_accounts()
        config.save()
        self.reload_app()

    def account_button_click(self, account_index):
        lib.open_steam_in_account(account_index)

    def account_button_right_click(self, account_index, event):
        lib.config.remove_account(account_index)
        lib.config.save()
        self.reload_app()

    def create_accounts_frame(self):
        self.accounts_frame = ck.CTkFrame(self)
        self.accounts_frame.pack(padx=10, pady=10)
        if len(config.get_accounts()) == 0:
            self.accounts_frame.pack_forget()

        for (account_index, account_title) in enumerate(config.get_account_titles()):
            callback = partial(self.account_button_click, account_index)
            self.account_box = AccountBox(
                self.accounts_frame, width=250, height=75, title=account_title, avatar_size=34, command=callback)
            self.account_box.account_index = account_index
            right_click_callback = partial(
                self.account_button_right_click, account_index)
            self.account_box.bind("<ButtonRelease-3>",
                                  command=right_click_callback)
            self.account_box.pack(padx=5, pady=5)
        return self.accounts_frame

    '''Prompts the user with a dialog asking Username and Title, returns a tuple containg (title, username)'''

    def new_account_dialog(self):
        lib.keylistener.stop()

        username_dialog = ck.CTkInputDialog(
            text="Insert Account Username", title='Add Account')
        username = username_dialog.get_input()
        if username == None:
            return None
        title_dialog = ck.CTkInputDialog(
            text="Insert Account Title", title='Add Account')
        title = title_dialog.get_input()
        if title == None:
            return None

        lib.keylistener.start()
        return (title, username)

    def reload_app(self):
        self.accounts_frame.destroy()
        self.acoounts_frame = self.create_accounts_frame()

    def add_account_button_press(self):
        print("adding new account")
        account_data = self.new_account_dialog()
        if account_data == None:
            return
        title = account_data[0]
        username = account_data[1]

        account_index = lib.config.add_account(title, username)
        lib.config.save()
        callback = partial(self.account_button_click, account_index)
        button = ck.CTkButton(self.accounts_frame,
                              text=title, command=callback)
        button.pack(padx=5, pady=5)
        button.account_index = account_index
        self.reload_app()

    def __init__(self):
        super().__init__()
        self.wm_iconbitmap('Assets/Icon.ico')
        self.title("Steam Account Switcher")
        self.geometry("300x400")
        self.resizable(0, 0)

        self.topbar = ck.CTkFrame(self, width=450, height=100)
        self.topbar.pack(side="top", fill="x", expand=False)

        self.add_account_button = ck.CTkButton(
            self.topbar, text="+", command=self.add_account_button_press, width=50)
        self.add_account_button.grid(padx=10, pady=10, row=0, column=0)

        self.clear_account_button = ck.CTkButton(
            self.topbar, text="clear", width=80, command=self.clear_accounts_button_press)
        self.clear_account_button.grid(padx=10, pady=10, row=0, column=1)

        self.import_button = ck.CTkButton(
            self.topbar, text="import", width=100)
        self.import_button.grid(padx=10, pady=10, row=0, column=2)

        self.close_on_switch = ck.CTkSwitch(
            self, text='Close on switch', progress_color=("#326da8", "#326da8"), command=self.close_on_switch)
        self.close_on_switch.pack(
            side="bottom", padx=10, pady=10)
        if config.get_close_on_switch():
            self.close_on_switch.select()

        self.accounts_frame = self.create_accounts_frame()

        self.bind("<Unmap>", lambda _: lib.keylistener.stop())
        self.bind("<Map>", lambda _: lib.keylistener.start())

        self.mainloop()
        lib.terminate_app()
