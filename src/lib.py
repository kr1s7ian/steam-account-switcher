import os
import sys
import toml
import subprocess
import threading
import requests
from bs4 import BeautifulSoup
import vdf
import winreg

'''Closes the program'''


def terminate_app():
    os._exit(0)


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
                '=[["title1", "username1", ""]] \ncloseOnSwitch=true'
            f.write(empty_config)
            f.close()

    '''Setup config class'''

    def __init__(self):
        self.accounts_key = 'accounts'
        self.config_path = "config.toml"
        try:
            self.data = self.load()
        except:
            self.create_config_file()
            self.data = self.load()

    '''Returns close_on_switch bool from config'''

    def get_close_on_switch(self):
        return self.data["closeOnSwitch"]

    '''Sets close_on_switch bool to memory config'''

    def set_close_on_switch(self, new_value):
        self.data["closeOnSwitch"] = new_value

    '''Returns all the account entries in the config'''

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

    '''Returns account steamid specified by the account_index from the config file'''

    def get_account_steamid(self, index):
        return self.data[self.accounts_key][index][2]

    '''Sets account title specified by the account_index to new_title'''

    def set_account_title(self, index, new_title):
        self.data[self.accounts_key][index][0] = new_title

    '''Sets account username specified by the account_index to new_username'''

    def set_account_username(self, index, new_username):
        self.data[self.accounts_key][index][1] = new_username

    '''Appends a new account object to the config with title and username as its values.
     Returns index of newly added account'''

    def add_account(self, title, username, steamid):
        self.data[self.accounts_key].append([title, username, steamid])
        return len(self.get_accounts()) - 1

    '''Removes account specified by account_index from the config'''

    def remove_account(self, account_index):
        del self.data[self.accounts_key][account_index]

    def clear_accounts(self):
        self.data[self.accounts_key].clear()


'''Steam class containg all steam lib functions'''


class Steam:
    '''Setup Steam class'''

    def __init__(self):
        self.account_avatars_path = 'Assets/account_avatars'

    '''Returns steam path on the current machine, if not found returns None'''

    def get_steam_path(self):
        steam_path = ''
        try:
            hkey = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "Software\Valve\Steam")
        except:
            print("cannot locate steam reg files")

        try:
            steam_path = winreg.QueryValueEx(hkey, "SteamPath")[0]
        except:
            steam_path = None
            print("Unable to locate steam path")
        return steam_path

    '''Kills the steam process on the machine'''

    def kill_steam(self):
        subprocess.run(["taskkill.exe", "/F", "/IM", "steam.exe"],
                       capture_output=False, shell=True)
    '''Launches the steam process on the machine'''

    def open_steam(self):
        subprocess.call("start steam://open/main",
                        creationflags=subprocess.DETACHED_PROCESS, shell=True)

    '''Logins in the user specified by account index of config file'''

    def login_steam(self, account_index):
        global config
        username = config.get_account_usernames()[account_index]
        print("logging in " + username + " steam account")
        subprocess.call('reg add "HKCU\Software\Valve\Steam" /v AutoLoginUser /t REG_SZ /d ' +
                        username + ' /f', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
        subprocess.call('reg add "HKCU\Software\Valve\Steam" /v RememberPassword /t REG_DWORD /d 1 /f',
                        creationflags=subprocess.CREATE_NO_WINDOW, shell=True)

    '''Kills Steam process and logs into the account specified by account_index before launching steam.
    closes application based on close_on_switch bool'''

    def open_steam_in_account(self, account_index, close_on_switch: bool):
        self.kill_steam()
        self.login_steam(account_index)
        self.open_steam()
        if close_on_switch:
            terminate_app()

    '''Returns object containing all the steam logins information by parsing loginusers.vdf'''

    def load_login_users_vdf_file(self):
        steam_path = self.get_steam_path().replace('/', '\\')
        vdf_path = os.path.join(steam_path, 'config', 'loginusers.vdf')
        try:
            with open(vdf_path, 'r', encoding='utf-8') as vdf_file:
                return vdf.load(vdf_file)
        except:
            print('unable to locate loginusers.vdf in ' + vdf_path)

    '''Returns login usernames from loginusers.vdf file'''

    def get_login_users_names(self):
        loginusers_vdf = self.load_login_users_vdf_file()
        account_names = []
        for user in loginusers_vdf['users'].values():
            account_names.append(user['AccountName'])
        return account_names

    '''Returns login steamids from loginusers.vdf file'''

    def get_login_users_steamids(self):
        loginusers_vdf = self.load_login_users_vdf_file()
        account_steamids = []
        for steamid in loginusers_vdf['users'].keys():
            account_steamids.append(steamid)
        return account_steamids

    '''Returns url of steam account avatar by steamid'''

    def get_user_avatar_url(self, steamid):
        if steamid == None or steamid == "":
            return None
        with requests.get('https://steamcommunity.com/profiles/{}'.format(steamid)) as r:
            steam_page = BeautifulSoup(r.content, features="html.parser")
        images = steam_page.find(
            'div', attrs={"class": 'playerAvatarAutoSizeInner'})
        try:
            profile_picture = images.findAll('img')[1]['src']
        except:
            try:
                profile_picture = images.findAll('img')[0]['src']
            except:
                profile_picture = None
        return profile_picture

    '''Downloads steam account avatar by steamid, and saves it to output path'''

    def download_user_avatar(self, steamid, output):
        if steamid == None:
            return None
        if not os.path.exists(self.account_avatars_path):
            os.makedirs(self.account_avatars_path)
        avatar_url = self.get_user_avatar_url(steamid)
        avatar_data = requests.get(avatar_url).content

        with open(output, 'wb') as handler:
            handler.write(avatar_data)

    '''Returns steam account avatar path by steamid if found,
     if not found it downloads the avatar image and returns it's path'''

    def get_user_avatar_path(self, steamid):
        if steamid == None or steamid == "":
            return None
        user_avatar_path = os.path.join(
            self.account_avatars_path, steamid,).replace('/', '\\') + ".jpg"
        if os.path.exists(user_avatar_path):
            return user_avatar_path
        else:
            self.download_user_avatar(steamid, user_avatar_path)
        return user_avatar_path


config = Config()
steam = Steam()
