# steam-account-switcher
GUI Steam account switcher made with customtkinter py.

How To Use:
- Use import button to auto import all previously logged in steam accounts.
- Use Keyboard keys 1 to 9 to log in in the respective accounts, in top to bottom order.
- Right clicking an account button will delete that entry.
- Pressing the plus button prompts the user for a new username along with a new title, the title is the text shown on the buttons, and username is the username of the steam account the button will log into.

![Program Demo Image](https://i.imgur.com/9j1AIOd.png)

Ignore if using releases:
- If you are cloning and running with python, know that customtkinter has a known bug with the CTkInputDialog, it should return None when pressing cancel on an input dialog box, but the behaviour of the dialog box is set to be the same for the cancel button and the ok button. For more details on how fix the issue go here https://github.com/TomSchimansky/CustomTkinter/pull/853/commits/d43cc3d6112c77db7742156198b2014ce5f56058 

Other:
- Feel free to submit feedback in the issues tab, even if you feel its a minor detail or if you have any problems:
- Idea of the tool and  functionality of the account switching mechanics by pog
#5249, python code and implementation of UI made by me.
