import tkinter as tk
from DatabaseHandler import DatabaseHandler


class DeleteCategoryWindow:
    def __init__(self, master, category, notebook):
        self.top = tk.Toplevel(master)
        self.top.geometry("500x60")
        self.category = category
        self.notebook = notebook

        self.label_frame = tk.Frame(master=self.top)
        self.label_frame.pack(side=tk.TOP)
        self.label = tk.Label(master=self.label_frame, text="Do you really wish to delete " +
                                                            self.category.get_name() + " category?")
        self.label.config(font=("verdana", 13), fg="DarkOrange1")

        self.buttons_frame = tk.Frame(master=self.top)
        self.buttons_frame.pack(side=tk.TOP)

        self.yes = tk.Button(master=self.buttons_frame, text="Yes", command=self.delete_category)
        self.yes.config(font=("verdana", 13), fg="DarkOrange1")

        self.no = tk.Button(master=self.buttons_frame, text="No", command=self.no)
        self.no.config(font=("verdana", 13), fg="DarkOrange1")

        self.label.pack(side=tk.LEFT)
        self.yes.pack(side=tk.LEFT)
        self.no.pack(side=tk.LEFT)

    def delete_category(self):
        self.notebook.forget(self.notebook.select())
        DatabaseHandler.delete_category(self.category)
        self.top.destroy()

    def no(self):
        self.top.destroy()
