import tkinter as tk
from DatabaseHandler import DatabaseHandler
from InvalidInputWindow import InvalidInputWindow
from FoodFrame import FoodFrame
from datetime import  datetime


class AddFoodWindow:
    def __init__(self, master, application, category, tab, favorite_tab, expired_tab):
        self.master = master
        self.top = tk.Toplevel(master)
        self.application = application
        self.category = category
        self.tab = tab
        self.favorite_tab = favorite_tab
        self.expired_tab = expired_tab

        self.top.geometry("200x160")
        self.label_frame = tk.Frame(master=self.top)
        self.label_frame.pack(side=tk.TOP)
        self.label = tk.Label(master=self.label_frame, text="New Food:")
        self.label.config(font=("verdana", 13), fg="DarkOrange1")
        self.label.pack(side=tk.TOP)
        self.entry = tk.Entry(master=self.top, font=("verdana", 13), fg="white",
                              bg="DarkOrange1", bd=1, relief=tk.SOLID, justify="center")
        self.entry.pack(side=tk.TOP)
        self.value = None

        # label and entry for month
        self.month_frame = tk.Frame(master=self.top)
        self.month_frame.pack(side=tk.TOP)

        self.month_label = tk.Label(master=self.month_frame, text="Month:")
        self.month_label.config(font=("verdana", 13), fg="DarkOrange1")
        self.month_label.pack(side=tk.LEFT, anchor="w")
        self.date_entry_month = tk.Entry(master=self.month_frame, font=("verdana", 13), fg="white",
                                         bg="DarkOrange1", bd=1, relief=tk.SOLID, width=5, justify="center")
        self.date_entry_month.pack(side=tk.RIGHT, anchor="e")

        # label and entry for day
        self.day_frame = tk.Frame(master=self.top)
        self.day_frame.pack(side=tk.TOP)

        self.day_label = tk.Label(master=self.day_frame, text="Day:")
        self.day_label.config(font=("verdana", 13), fg="DarkOrange1")
        self.day_label.pack(side=tk.LEFT, anchor="w")
        self.date_entry_day = tk.Entry(master=self.day_frame, font=("verdana", 13), fg="white",
                                       bg="DarkOrange1", bd=1, relief=tk.SOLID, width=5, justify="center")
        self.date_entry_day.pack(side=tk.RIGHT, anchor="e")

        # label and entry for year
        self.year_frame = tk.Frame(master=self.top)
        self.year_frame.pack(side=tk.TOP)

        self.year_label = tk.Label(master=self.year_frame, text="Year:")
        self.year_label.config(font=("verdana", 13), fg="DarkOrange1")
        self.year_label.pack(side=tk.LEFT, anchor="w")
        self.date_entry_year = tk.Entry(master=self.year_frame, font=("verdana", 13), fg="white",
                                        bg="DarkOrange1", bd=1, relief=tk.SOLID, width=5, justify="center")
        self.date_entry_year.pack(side=tk.RIGHT, anchor="e")

        self.button = tk.Button(master=self.top, text="Create food", command=self.clean)
        self.button.pack_propagate()
        self.button.config(font=("verdana", 13), fg="DarkOrange1")
        self.button.pack(side=tk.TOP)

    def clean(self):
        name = self.entry.get()
        month = self.date_entry_month.get()
        day = self.date_entry_day.get()
        year = self.date_entry_year.get()
        if self.valid_date_checker(month, day, year):
            food = DatabaseHandler.create_food(self.category, name, month + "/" + day + "/" + year)
            if food:
                expire = False
                month = food.get_expiration_date().split("/")[0]
                day = food.get_expiration_date().split("/")[1]
                year = food.get_expiration_date().split("/")[2]
                string = datetime.today().strftime("%m/%d/%Y").split(" ")[0]
                if int(year) < int(string.split("/")[2]):
                    expire = True
                elif int(year) == int(string.split("/")[2]):
                    if int(month) < int(string.split("/")[0]):
                        expire = True
                    elif int(month) == int(string.split("/")[0]):
                        if int(day) < int(string.split("/")[1]):
                            expire = True
                if expire:
                    food.set_as_expired()
                new_frame = FoodFrame(self.tab.tab_frame, food, self.category,
                                      self.favorite_tab, self.expired_tab, self.application)
                self.tab.add_frame(new_frame)
                self.top.destroy()
            else:
                InvalidInputWindow(self.master, self.application,
                                   "Food with this name and expiration date already exists.")
        else:
            InvalidInputWindow(self.master, self.application, "Invalid date entered.")

    @staticmethod
    def valid_date_checker(month, day, year):
        try:
            day = int(day)
            month = int(month)
            year = int(year)

            if (0 < month < 8 and month % 2 == 1) or (13 > month > 7 and month % 2 == 0):
                if day < 1 or day > 31:
                    return False
            elif 0 < month < 13 and month != 2:
                if day < 1 or day > 30:
                    return False
            elif month == 2:
                if year % 4 == 0:
                    if year % 100 == 0:
                        if year % 400 == 0:
                            if day < 0 or day > 29:
                                return False
                        else:
                            if day < 0 or day > 28:
                                return False
                else:
                    if day < 0 or day > 28:
                        return False
            else:
                return False

        except ValueError:
            return False
        return True













