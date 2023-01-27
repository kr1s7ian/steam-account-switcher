import os
import sys
import toml
import subprocess
import threading
from keylistener import KeyListener

'''Closes the steam process using taskkill'''


def kill_steam():
    subprocess.run(["taskkill.exe", "/F", "/IM", "steam.exe"],
                   capture_output=False, shell=True)


'''Open steam process using start'''


def open_steam():
    subprocess.call("start steam://open/main",creationflags=subprocess.DETACHED_PROCESS, shell=True)


'''Login in steam account with username parameter using registers red add'''


def login_steam(account_index):
    global config
    username = config.get_account_usernames()[account_index]
    print("logging in " + username + " steam account")
    subprocess.call('reg add "HKCU\Software\Valve\Steam" /v AutoLoginUser /t REG_SZ /d ' +username+ ' /f', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    subprocess.call('reg add "HKCU\Software\Valve\Steam" /v RememberPassword /t REG_DWORD /d 1 /f', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)


'''Closes all processes related to the app'''


def terminate_app():
    keylistener.kill()
    os._exit(0)


'''Opens steam in the steam account specified by account index, quit_on_switch is 
a bool that decides if the app should be closed after the account switch'''


def open_steam_in_account(account_index, quit_on_switch):
    kill_steam()
    login_steam(account_index)
    open_steam()

    if quit_on_switch:
        terminate_app()


'''Config class that contains all config related logic and variables'''


class Config:
    '''Loads config file in memory and returns an object representing its data'''

    def load(self):
        with open(self.config_path, 'r') as f:
            return toml.load(f)

    '''Saves the in memory version of the config to the config file on the disk'''

    def save(self):
        with open(self.config_path, 'w') as f:
            toml.dump(self.data, f)
    '''creates fresh config file with title1 and username1 values'''

    def create_config_file(self):
        with open(self.config_path, 'w') as f:
            empty_config = self.accounts_key + \
                R'= [["title1", "username1"]]'
            f.write(empty_config)
            f.close()

    def __init__(self):
        self.accounts_key = 'accounts'
        self.config_path = "config.toml"
        try:
            self.data = self.load()
        except:
            self.create_config_file()
            self.data = self.load()

    '''Returns all accounts (an array of a list which contains account usernames and titles)'''

    def get_accounts(self):
        return self.data[self.accounts_key]

    '''Returns a list of all account usernames'''

    def get_account_usernames(self):
        usernames = []
        for account in self.get_accounts():
            # index 0 is titles, index 1 is usernames
            usernames.append(account[1])
        return usernames

    '''Returns a list of all account titles'''

    def get_account_titles(self):
        titles = []
        for account in self.get_accounts():
            # index 0 is titles, index 1 is usernames
            titles.append(account[0])
        return titles
    '''Returns account object that contains account title and username specified by the account_index from the config file'''

    def get_account(self, index):
        return self.data[self.accounts_key][index]

    '''Returns account title object specified by the account_index from the config file'''

    def get_account_title(self, index):
        return self.data[self.accounts_key][index][0]

    '''Returns account username object specified by the account_index from the config file'''

    def get_account_username(self, index):
        return self.data[self.accounts_key][index][1]

    '''Sets account title specified by the account_index to new_title'''

    def set_account_title(self, index, new_title):
        self.data[self.accounts_key][index][0] = new_title

    '''Sets account username specified by the account_index to new_username'''

    def set_account_username(self, index, new_username):
        self.data[self.accounts_key][index][1] = new_username

    '''Appends a new account object to the config with title and username as its values.
     Returns index of newly added account'''

    def add_account(self, title, username):
        self.data[self.accounts_key].append([title, username])
        return len(self.get_accounts()) - 1

    '''Removes account specified by account_index from the config'''

    def remove_account(self, account_index):
        del self.data[self.accounts_key][account_index]


config = Config()
keylistener = KeyListener()
