import customtkinter as ck
from typing import Callable
from PIL import Image
from PIL import PngImagePlugin


def get_placeholder_image(size):
    return ck.CTkImage(Image.open('Logo.png'), size=(size, size))


class AccountBox(ck.CTkFrame):
    def bind(self, sequence=None, command=None, add=True):
        """ called on the tkinter.Canvas """
        if not (add == "+" or add is True):
            raise ValueError(
                "'add' argument can only be '+' or True to preserve internal callbacks")
        self.button.bind(sequence, command, add=True)

    def unbind(self, sequence=None, funcid=None):
        """ called on the tkinter.Canvas """
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None, because there is a bug in" +
                             " tkinter and its not clear whether the internal callbacks will be unbinded or not")
        self.self.button.unbind(sequence, None)

    def __init__(self, *args,
                 image: ck.CTkImage = None,
                 title: str,
                 height: int,
                 width: int,
                 command: Callable = None,
                 avatar_size: int,
                 ** kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        if image == None:
            self.avatar_image = get_placeholder_image(avatar_size)
        else:
            self.avatar_image = image.configure(
                size=(avatar_size, avatar_size))

        self.avatar = ck.CTkLabel(self, image=self.avatar_image, text="")
        self.avatar.grid(padx=5, pady=5, row=0, column=0)

        button_width = (width - avatar_size) - 15

        self.button = ck.CTkButton(
            self, text=title, height=avatar_size, width=button_width, command=command)
        self.button.grid(padx=5, pady=5, row=0, column=1)
