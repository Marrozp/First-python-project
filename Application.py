import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from FavoriteTab import FavoriteTab
from ExpiredTab import ExpiredTab

from DatabaseHandler import DatabaseHandler as Handler
from Tab import Tab
from AddCategoryWindow import AddCategoryWindow


class Application:
    def __init__(self, *args, **kwargs):
        self.banner = tk.Frame(root, height=150, bg="blue")
        self.banner.pack_propagate(False)
        self.banner.pack(side=tk.TOP, fill=tk.X)

        self.banner_canvas = tk.Canvas(self.banner, bg="DarkOrange1")
        self.banner_canvas.pack_propagate(False)
        self.banner_canvas.pack(fill=tk.X)
        self.bg = ImageTk.PhotoImage(file="concept_bg.png")
        self.banner_canvas.create_image(962, 77, image=self.bg)
        self.fries = ImageTk.PhotoImage(file="burger_fries.png")
        self.banner_canvas.create_image(400, 80, image=self.fries)

        self.tabs_frame = tk.Frame(root, bg="white")
        self.tabs_frame.pack_propagate(False)
        self.tabs_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.tabs_frame)
        self.notebook.pack(anchor="nw", fill=tk.BOTH, expand=True)

        self.favorites_image = tk.PhotoImage(file="click_favorite.png")
        self.expired_image = tk.PhotoImage(file="exclamation4_4.png")

        # frame for add button
        self.add_frame = tk.Frame(self.banner_canvas, height=35, width=65, bg="blue")
        self.add_frame.pack_propagate(False)
        self.add_frame.pack(side=tk.BOTTOM, anchor="se")

        # canvas for add button
        self.add_canvas = tk.Canvas(self.add_frame, height=35, width=65)
        self.add_canvas.pack_propagate(False)
        self.add_canvas.pack(fill=tk.BOTH, expand=True)

        self.plus_image = tk.PhotoImage(file="plus_2.png")
        self.plus_created = self.add_canvas.create_image(13, 7, anchor="nw", image=self.plus_image)
        self.add_canvas.tag_bind(self.plus_created, "<Button-1>", self.add_category)

        # favorite and expired tab
        self.favorites_tab = None
        self.expired_tab = None
        self.tabs_list = []

    def add_tab(self, tab):
        self.tabs_list.append(tab)

    def add_category(self, event):
        window = AddCategoryWindow(self.notebook, self, self.favorites_tab, self.expired_tab)

    def get_notebook(self):
        return self.notebook

    def get_tabs_list(self):
        return self.tabs_list

    def populate(self, categories_list):
        self.favorites_tab = FavoriteTab(self.notebook, self, self.favorites_image)
        self.expired_tab = ExpiredTab(self.notebook, self, self.expired_image, self.favorites_tab)
        self.favorites_tab.set_expired_tab(self.expired_tab)
        for i in range(len(categories_list)):

            new_tab = Tab(self.notebook, categories_list[i], self, self.favorites_tab, self.expired_tab)
            new_tab.populate_tab()
            self.tabs_list.append(new_tab)

    @staticmethod
    def initiate_style():
        style = ttk.Style()
        style.theme_create("MyStyle", parent="vista", settings={
            "TNotebook.Tab": {"configure": {"font": ('verdana', '13'),
                                            "foreground": "DarkOrange1", "padding": [10, 5]},
                              }
        })
        style.configure("TNotebook.Tab", focuscolor=style.configure(".")["background"])
        style.theme_use("MyStyle")


def get_list():
    return Handler.get_categories_list()


root = tk.Tk()
root.geometry("800x600")
root.title("FoodCheck")


if __name__ == '__main__':
    app = Application(root)
    app.initiate_style()
    app.populate(get_list())
    root.mainloop()
