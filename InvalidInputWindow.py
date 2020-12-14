import tkinter as tk


class InvalidInputWindow:
    def __init__(self, master, application, message):
        self.top = tk.Toplevel(master)
        self.application = application
        self.message = message

        self.top.geometry("350x45")
        self.label = tk.Label(master=self.top, text=self.message)
        self.label.config(font=("verdana", 13), fg="DarkOrange1")

        self.label.pack()
