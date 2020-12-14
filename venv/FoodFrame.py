import tkinter as tk
from PIL import ImageTk
from DatabaseHandler import DatabaseHandler
from datetime import datetime

class FoodFrame:
    def __init__(self, master, food, category, favorites_tab, expired_tab, application, expiration_allowed=True):
        self.master = master
        self.food = food
        self.category = category
        self.favorites_tab = favorites_tab
        self.expired_tab = expired_tab
        self.application = application

        # frame for whole row
        self.sub_master = tk.Frame(self.master, height=35, bd=1, relief=tk.GROOVE)
        self.sub_master.pack_propagate(False)
        self.sub_master.pack(side=tk.TOP, anchor="nw", fill=tk.X)


        # frame for favorite button
        self.favorite_frame = tk.Frame(self.sub_master, height=35, width=65, bg="blue")
        self.favorite_frame.pack_propagate(False)
        self.favorite_frame.pack(side=tk.LEFT, anchor="w")

        # canvas for favorite button, struggle renaming
        self.canvas = tk.Canvas(self.favorite_frame, height=35, width=65)
        self.canvas.pack_propagate(False)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # def favorite click originally here without self attribute, also canvas.tag_bind last att was without self

        # favorite button
        self.favorite = ImageTk.PhotoImage(file="click_favorite.png")
        self.not_favorite = ImageTk.PhotoImage(file="not_favorites.png")

        # hocus pocus, edit: actually creates favorite button, cannot believe it works

        if self.food.is_favorite() == "1":
            self.pic_created = self.canvas.create_image(13, 7, anchor="nw", image=self.favorite)
        else:
            self.pic_created = self.canvas.create_image(13, 7, anchor="nw", image=self.not_favorite)
        self.canvas.tag_bind(self.pic_created, "<Button-1>", self.favorite_click)

        # label for food name
        self.food_label = tk.Label(master=self.sub_master, text=self.food.get_name(), width=30, anchor="w")
        self.food_label.config(font=("verdana", 13), fg="DarkOrange1")
        self.food_label.pack(side=tk.LEFT, anchor="w")

        # frame and canvas for food delete button
        self.delete = ImageTk.PhotoImage(file="delete_2.png")
        self.delete_frame = tk.Frame(master=self.sub_master, bg="blue", height=35, width=65)
        self.delete_frame.pack_propagate(False)
        self.delete_frame.pack(side=tk.RIGHT, anchor="w")
        self.delete_canvas = tk.Canvas(master=self.delete_frame)
        self.delete_image = self.delete_canvas.create_image(13, 7, anchor="nw", image=self.delete)
        self.delete_canvas.pack(side=tk.RIGHT, anchor="w")
        self.delete_canvas.tag_bind(self.delete_image, "<Button-1>", self.delete_click)


        #self.label = tk.Label(master=self.sub_master, text="add")
        #self.label.config(font=("verdana", 13))
        #self.label.pack(side=tk.RIGHT, anchor="w")

        # label for expiration date
        self.date_label = tk.Label(master=self.sub_master, text=self.food.get_expiration_date())
        self.date_label.config(font=("verdana", 13), fg="DarkOrange1")
        self.date_label.pack(side=tk.LEFT, anchor="w")

        # config for expired food
        if self.food.already_expired():
            self.food_label.configure(bg="tomato", fg="#f0f0f0")
            self.date_label.configure(bg="tomato", fg="#f0f0f0")
            if expiration_allowed:
                self.expired_tab.add_food(self.food, self.category)

    def get_canvas(self):
        return self.canvas

    def get_not_favorite_pic(self):
        return self.not_favorite

    def get_favorite_pic(self):
        return self.favorite

    def favorite_click(self, event):
        if self.food.is_favorite() == "1":
            self.canvas.itemconfigure(self.pic_created, image=self.not_favorite)
            DatabaseHandler.unfavorite(self.category, self.food)
            self.favorites_tab.delete_frame(self.food)
            for frame in self.expired_tab.get_frames():
                if self.food == frame.get_food():
                    frame.get_canvas().itemconfigure(self.pic_created, image=self.not_favorite)
            for tab in self.application.get_tabs_list():
                if tab.get_category() == self.category:
                    for frame in tab.get_frames():
                        if frame.get_food() == self.food:
                            frame.get_canvas().itemconfigure(self.pic_created, image=frame.get_not_favorite_pic())
        else:
            self.canvas.itemconfigure(self.pic_created, image=self.favorite)
            DatabaseHandler.set_favorite(self.category, self.food)
            new_frame = FoodFrame(self.favorites_tab.get_tab_frame(), self.food, self.category,
                                  self.favorites_tab, self.expired_tab, self.application, False)
            self.favorites_tab.add_frame(new_frame)
            for frame in self.expired_tab.get_frames():
                if self.food == frame.get_food():
                    frame.get_canvas().itemconfigure(self.pic_created, image=self.favorite)
            for tab in self.application.get_tabs_list():
                if tab.get_category() == self.category:
                    for frame in tab.get_frames():
                        if frame.get_food() == self.food:
                            frame.get_canvas().itemconfigure(self.pic_created, image=frame.get_favorite_pic())


    def delete_click(self, event):
        DatabaseHandler.delete_food(self.category, self.food)
        if self.food.is_favorite() == "1":
            self.favorites_tab.delete_frame(self.food)
        if self.food.already_expired():
            self.expired_tab.delete_frame(self.food)
        for tab in self.application.get_tabs_list():
            if tab.get_category() == self.category:
                for frame in tab.get_frames():
                    if frame.get_food() == self.food:
                        frame.sub_master.destroy()

    def get_food(self):
        return self.food

    def get_sub_master(self):
        return self.sub_master
