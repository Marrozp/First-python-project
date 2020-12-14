import tkinter as tk
from tkinter import ttk

from FoodFrame import FoodFrame
from AddFoodFrame import AddFoodFrame
from PIL import ImageTk
from Category import Category


class Tab:
    def __init__(self, notebook, category, application, favorite_tab, expired_tab, image=False):
        self.application = application
        tab_frames_style = ttk.Style()
        tab_frames_style.configure('TFrame', background='snow2')
        self.tab_frame = ttk.Frame()
        self.favorite_tab = favorite_tab
        self.expired_tab = expired_tab
        self.category = category
        self.frames = []
        self.image = image
        self.notebook = notebook
        if not image:
            notebook.add(self.tab_frame, text=self.category.get_name())
        else:
            notebook.add(self.tab_frame, image=image)

    def get_category(self):
        return self.category

    def get_tab_frame(self):
        return self.tab_frame

    def get_frames(self):
        return self.frames

    def add_frame(self, frame):
        self.frames.append(frame)

    def populate_tab(self):

        frame = AddFoodFrame(self.tab_frame, self.application, self.category,
                             self, self.notebook, self.favorite_tab, self.expired_tab)

        for food in self.category.get_foods():
            if food.is_favorite() == "1":
                self.favorite_tab.add_food(food, self.category)
            frame = FoodFrame(self.tab_frame, food, self.category,
                              self.favorite_tab, self.expired_tab, self.application)
            self.frames.append(frame)
