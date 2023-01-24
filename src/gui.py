import customtkinter as ck
from functools import partial
import os
import lib
from lib import config


class Gui(ck.CTk):
    def account_button_click(self, account_index):
        lib.open_steam_in_account(account_index, self.close_on_switch.get())

    def account_button_right_click(self, account_index, event):
        lib.config.remove_account(account_index)
        lib.config.save()
        self.reload_app()

    def create_accounts_frame(self):
        self.accounts_frame = ck.CTkFrame(self.bg)
        self.accounts_frame.pack(padx=5, pady=5)

        for (account_index, account_title) in enumerate(config.get_account_titles()):
            callback = partial(self.account_button_click, account_index)
            self.button = ck.CTkButton(
                self.accounts_frame, text=account_title, command=callback)

            self.button.account_index = account_index
            right_click_callback = partial(
                self.account_button_right_click, account_index)
            self.button.bind("<ButtonRelease-3>",
                             command=right_click_callback)
            self.button.pack(padx=5, pady=5)

    '''Prompts the user with a dialog asking Username and Title, returns a tuple containg (title, username)'''

    def new_account_dialog(self):
        lib.keylistener.stop()

        username_dialog = ck.CTkInputDialog(text="Insert Account Username", title='Add Account')
        username = username_dialog.get_input()
        title_dialog = ck.CTkInputDialog(text="Insert Account Title", title='Add Account')
        title = title_dialog.get_input()

        lib.keylistener.start()
        return (title, username)

    def reload_app(self):
        self.destroy()
        Gui()

    def add_account_button_press(self):
        print("adding new account")
        account_data = self.new_account_dialog()
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
        self.title("Steam Account Switcher")
        self.geometry("600x500")
        self.resizable(0, 0)

        self.bg = ck.CTkFrame(self)
        self.bg.pack(padx=15, pady=15, fill="both", expand=True)

        self.label = ck.CTkLabel(master=self.bg, text='Steam Account Switcher', font=('Arialbd',40))
        self.label.pack(padx=10, pady=10)


        self.frame = ck.CTkFrame(self.bg)
        self.frame.pack(padx=5, pady=15)
        

        self.close_on_switch = ck.CTkSwitch(
            self.frame, text='Close on switch')
        self.close_on_switch.pack(padx=5, pady=5)
        self.close_on_switch.toggle()

        self.add_account_button = ck.CTkButton(
            self.frame, text="+", command=self.add_account_button_press)
        self.add_account_button.pack(padx=5, pady=5)

        self.accounts_frame = self.create_accounts_frame()

        self.mainloop()
        lib.terminate_app()