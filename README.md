# steam-account-switcher
Gui account switcher made with customtkinter py

Idea of the tool, and functionality of the account switching mechanics by pog
#5249, python code and implementation of UI made by me.

Ignore if using releases:
-If you are cloning and running with python, customtkinter has a known bug with the CTkInputDialog, it shold return None when pressing cancel but the command parameter is set to the same one for the ok button, for more details on how to the issue go here https://github.com/TomSchimansky/CustomTkinter/pull/853/commits/d43cc3d6112c77db7742156198b2014ce5f56058 

How To Use:
- Pressing the plus button prompts the user for a new username along with a new title, the title is the text shown on the buttons, and username is the username of the steam account the button will log into.
- Right clicking an account button will delete that entry.
- You can use keyboard keys 1 to 9 to log in in the respective accounts.

Other:
- Feel free to submit feedback in the issues tab, even if you feel its a minor detail or if you have any problems:

