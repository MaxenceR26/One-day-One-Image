import json
import os
import tkinter as tk

from data.data import _token


class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        # Parameter colors
        print(os.getcwd())

        self.color = {
            'grey': '#2F2F2F',
            'light_grey': '#C4C4C4',
            'white': '#FFFFFF',
        }

        # Parameter interface

        self.geometry("700x150")
        self.title('Add your token !')
        self.iconbitmap('./LOGO APP/logo.ico')
        self.config(bg=self.color['grey'])

        # Text ; Entry ; Button

        self.title = tk.Label(self, text="Token", bg=self.color['grey'], fg=self.color['white'],
                              font=('Arial', 28, 'bold'))
        self.title.pack()

        self.entry = tk.Entry(self, bd=0)
        self.entry.pack(ipady=5, ipadx=110, pady=10)
        self.entry['justify'] = 'center'

        self.add_btn = tk.Button(self, text="Add", bg=self.color['grey'], fg=self.color['white'],
                                 font=('Arial', 12, 'bold'), bd=1, activebackground=self.color['grey'],
                                 activeforeground=self.color['white'], command=self.dump_token)
        self.add_btn.pack(pady=2, ipadx=15)

        self.mainloop()

    def dump_token(self):
        token = self.entry.get()
        _token(token)

Main()
