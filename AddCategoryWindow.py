from tkinter import ttk
import tkinter as tk
from DatabaseHandler import DatabaseHandler
from Tab import Tab
from Category import Category
from InvalidInputWindow import InvalidInputWindow


class AddCategoryWindow:
    def __init__(self, master, application, favorites_tab, expired_tab):
        self.master = master
        self.application = application
        self.favorites_tab = favorites_tab
        self.expired_tab = expired_tab
        self.top = tk.Toplevel(master)
        self.top.geometry("200x80")
        self.label = tk.Label(master=self.top, text="New Category:")
        self.label.config(font=("verdana", 13), fg="DarkOrange1")
        self.label.pack(side=tk.TOP)
        self.entry = tk.Entry(master=self.top, font=("verdana", 13), fg="white",
                              bg="DarkOrange1", bd=1, relief=tk.SOLID, justify="center")
        self.entry.pack(side=tk.TOP)
        self.value = None
        self.button = tk.Button(master=self.top, text="Create category", command=self.clean)
        self.button.pack_propagate()
        self.button.config(font=("verdana", 13), fg="DarkOrange1")
        self.button.pack(side=tk.TOP)

    def clean(self):
        used = False
        for tab in self.application.tabs_list:
            if tab.get_category().get_name() == self.entry.get():
                used = True
        if used:
            window = InvalidInputWindow(self.master, self.application,
                                        "This category already exists.")
        else:

            if self.valid_input_checker(self.entry.get()):
                self.value = self.entry.get()
                DatabaseHandler.create_category_database(self.entry.get())
                new_tab = Tab(self.application.get_notebook(),
                              Category(self.entry.get()), self.application, self.favorites_tab, self.expired_tab)
                new_tab.populate_tab()
                self.application.tabs_list.append(new_tab)
                self.top.destroy()
            else:
                window = InvalidInputWindow(self.master, self.application,
                                            "Use only capital and lowercase letters,\nnumbers or apostrophe, please.")

    @staticmethod
    def valid_input_checker(string):
        is_valid = True
        for letter in string:
            a = ord(letter)
            if not (64 < a < 91 or 96 < a < 123 or a == ord("'") or letter.isnumeric() or a == ord(" ")):
                is_valid = False
        return is_valid








