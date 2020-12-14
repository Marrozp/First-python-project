import tkinter as tk
from PIL import ImageTk
from AddFoodWindow import AddFoodWindow
from DeleteCategoryWindow import DeleteCategoryWindow


class AddFoodFrame:
    def __init__(self, master, application, category, tab, notebook, favorite_tab, expired_tab):
        self.application = application
        self.master = master
        self.category = category
        self.tab = tab
        self.notebook = notebook
        self.favorite_tab = favorite_tab
        self.expired_tab = expired_tab

        # frame for whole row
        self.sub_master = tk.Frame(self.master, height=35, bd=1, relief=tk.GROOVE)
        self.sub_master.pack_propagate(False)
        self.sub_master.pack(side=tk.TOP, anchor="nw", fill=tk.X)
        self.plus_image = tk.PhotoImage(file="burger_3.png")
        self.plus_canvas = tk.Canvas(self.sub_master, height=35, width=65)
        self.plus_canvas.pack(side=tk.LEFT)
        self.master.plus_image = self.plus_image
        self.created_plus_image = self.plus_canvas.create_image(12, 18, anchor="w", image=self.plus_image)
        self.plus_canvas.tag_bind(self.created_plus_image, "<Button-1>", self.add_food)

        self.del_image = tk.PhotoImage(file="delete_2.png")
        self.del_canvas = tk.Canvas(self.sub_master, height=35, width=65)
        self.del_canvas.pack(side=tk.LEFT, fill=tk.BOTH, anchor="w")
        self.master.del_image = self.del_image
        self.created_del_image = self.del_canvas.create_image(12, 18, anchor="w", image=self.del_image)
        self.del_canvas.tag_bind(self.created_del_image, "<Button-1>", self.delete_category)

    def add_food(self, event):
        window = AddFoodWindow(self.sub_master, self.application, self.category,
                               self.tab, self.favorite_tab, self.expired_tab)

    def delete_category(self, event):
        window = DeleteCategoryWindow(self.sub_master, self.category, self.notebook)
