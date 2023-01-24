import os
import sys
import toml

'''Closes the steam process using taskkill'''


def kill_steam():
    os.system("taskkill.exe /F /IM steam.exe")


'''Open steam process using start'''


def open_steam():
    os.system("start steam://open/main")


'''Login in steam account with username parameter using registers red add'''


def login_steam(account_index):
    global config
    username = config.get_account_usernames()[account_index]
    print("logging in " + username + " steam account")
    os.system(
        F'reg add "HKCU\Software\Valve\Steam" /v AutoLoginUser /t REG_SZ /d '+username+' /f')
    os.system(
        F'reg add "HKCU\Software\Valve\Steam" /v RememberPassword /t REG_DWORD /d 1 /f')


'''Config class that contains all config related logic and variables'''


class Config:
    def load(self):
        with open(self.config_path, 'r') as f:
            return toml.load(f)

    def save(self):
        with open(self.config_path, 'w') as f:
            toml.dump(self.data, f)

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

    def get_account(self, index):
        return self.data[self.accounts_key][index]

    def get_account_title(self, index):
        return self.data[self.accounts_key][index][0]

    def get_account_username(self, index):
        return self.data[self.accounts_key][index][1]

    def set_account_title(self, index, new_title):
        self.data[self.accounts_key][index][0] = new_title

    def set_account_username(self, index, new_username):
        self.data[self.accounts_key][index][1] = new_username

    def add_account(self, title, username):
        self.data[self.accounts_key].append([title, username])
        return len(self.get_accounts()) - 1

    def remove_account(self, account_index):
        del self.data[self.accounts_key][account_index]


config = Config()
