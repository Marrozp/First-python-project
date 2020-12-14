from AddCategoryWindow import AddCategoryWindow

from tkinter import ttk
import tkinter as tk


class AddTab:
    def __init__(self, notebook, application, image=False):
        self.application = application
        tab_frames_style = ttk.Style()
        tab_frames_style.configure('TFrame', background='snow2')
        self.notebook = notebook
        self.tab_frame = ttk.Frame()
        self.plus_image = tk.PhotoImage(file="plus.png")
        notebook.add(self.tab_frame, image=self.plus_image)
        self.tab_frame.bind("<Button-1>", self.add_category)
        #self.tab_frame.tag_bind(self.plus_image, "<Button-1>", self.add_category)

    def add_category(self, event):
        window = AddCategoryWindow(self.notebook, self.application)
        print(window.value)
