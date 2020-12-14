import sqlite3
import os
from datetime import datetime

from Category import Category

from Food import Food


class DatabaseHandler:

    @staticmethod
    def get_categories_list():
        categories_list = []
        for filename in os.listdir("D:/projekty/FoodCheck/databases"):
            name = (filename.split("."))[0]
            new_category = Category(name)
            """
            if name == "Favorites":
                categories_list.insert(0, new_category)
            elif name == "Expired":
                categories_list.insert(0, new_category)
            else:
                categories_list.append(new_category)
            """
            categories_list.append(new_category)
            new_category.set_foods_list(DatabaseHandler.get_foods_list(name))

        return categories_list

    @staticmethod
    def get_foods_list(name):

        food_list = []
        with sqlite3.connect("D:/projekty/FoodCheck/databases/" + name + ".db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Food")
            fetch = cursor.fetchall()
            for row in fetch:
                new_food = Food(row[0], row[1], row[2])
                food_list.append(new_food)

        return DatabaseHandler.divide_and_sort_lists(food_list)

    @staticmethod
    def create_category_database(name):

        if (name + ".db") in os.listdir("D:/projekty/FoodCheck/databases/"):
            return False

        with sqlite3.connect("D:/projekty/FoodCheck/databases/" + name + ".db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS Food(
                Name TEXT NOT NULL UNIQUE,
                ExpirationDate TEXT NOT NULL,
                Favorite TEXT
                );"""
            )
        return True

    @staticmethod
    def check_food_duplicates(category, name, expiration_date):
        data = (name, expiration_date)
        query = """SELECT EXISTS(SELECT 1 FROM Food where Name = ? AND ExpirationDate = ?)"""
        try:
            with sqlite3.connect("D:/projekty/FoodCheck/databases/" + category.get_name() + ".db") as connection:
                cursor = connection.cursor()
                cursor.execute(query, data)
                return cursor.fetchone()
        except sqlite3.IntegrityError:
            print("Category does not exist.")

    @staticmethod
    def create_food(category, name, expiration_date):
        print(DatabaseHandler.check_food_duplicates(category, name, expiration_date)[0])
        if DatabaseHandler.check_food_duplicates(category, name, expiration_date)[0] == 0:
            data = (name, expiration_date, "0")
            try:
                with sqlite3.connect("D:/projekty/FoodCheck/databases/" + category.get_name() + ".db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO Food VALUES(?, ?, ?);", data)
                new_food = Food(name, expiration_date, "0")
                category.add_food(new_food)
                return new_food
            except sqlite3.IntegrityError:
                print("Something went wrong when loading database connection.")
        else:
            return False

    @staticmethod
    def delete_category(category):
        os.remove("D:/projekty/FoodCheck/databases/" + category.get_name() + ".db")

    @staticmethod
    def delete_food(category, food):
        delete_query = """DELETE from Food where Name = ?"""
        data = food.get_name()
        """
        if int(food.is_favorite()) == 1:
            with sqlite3.connect("D:/projekty/FoodCheck/databases/Favorites.db") as connection:
                cursor = connection.cursor()
                cursor.execute(delete_query, (data,))
        """
        with sqlite3.connect("D:/projekty/FoodCheck/databases/" + category.get_name() + ".db") as connection:
            cursor = connection.cursor()
            cursor.execute(delete_query, (data,))

    @staticmethod
    def set_favorite(category, food):
        if not int(food.is_favorite()):
            category_data = (food.get_name(), food.get_expiration_date())
            category_query = """UPDATE Food set Favorite = True where Name = ? AND ExpirationDate = ?"""
            """
            favorite_data = (food.get_name(), food.get_expiration_date(), "1")
            favorite_query = "INSERT INTO Food VALUES(?, ?, ?)"
            """

            with sqlite3.connect("D:/projekty/FoodCheck/databases/" + category.get_name() + ".db") as connection:
                cursor = connection.cursor()
                cursor.execute(category_query, category_data)
            """
            with sqlite3.connect("D:/projekty/FoodCheck/databases/Favorites.db") as connection:
                cursor = connection.cursor()
                cursor.execute(favorite_query, favorite_data)
            """
            food.set_favorite("1")
        else:
            print("Food already added to favorites.")

    @staticmethod
    def unfavorite(category, food):
        if int(food.is_favorite()):
            category_data = (food.get_name(), food.get_expiration_date())
            category_query = """UPDATE Food set Favorite = 0 where Name = ? AND ExpirationDate = ?"""
            """
            favorite_data = (food.get_name(), food.get_expiration_date())
            favorite_query = "DELETE from Food where Name = ? AND ExpirationDate = ?"
            """

            with sqlite3.connect("D:/projekty/FoodCheck/databases/" + category.get_name() + ".db") as connection:
                cursor = connection.cursor()
                cursor.execute(category_query, category_data)
            """
            with sqlite3.connect("D:/projekty/FoodCheck/databases/Favorites.db") as connection:
                cursor = connection.cursor()
                cursor.execute(favorite_query, favorite_data)
            """
            food.set_favorite("0")
        else:
            print("Food already added to favorites.")

    @staticmethod
    def divide_and_sort_lists(food_list):
        favorite_expired = []
        expired = []
        favorite = []
        basic = []
        expire = False
        for food in food_list:
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
                if food.is_favorite() == "1":
                    favorite_expired.append(food)
                else:
                    expired.append(food)
            else:
                if food.is_favorite() == "1":
                    favorite.append(food)
                else:
                    basic.append(food)

            expire = False

        return DatabaseHandler.sort_food(favorite_expired) + DatabaseHandler.sort_food(expired) + \
               DatabaseHandler.sort_food(favorite) + DatabaseHandler.sort_food(basic)

    @staticmethod
    def sort_food(food_list):
        n = len(food_list)
        for i in range(n):
            # Create a flag that will allow the function to
            # terminate early if there's nothing left to sort
            already_sorted = True

            # Start looking at each item of the list one by one,
            # comparing it with its adjacent value. With each
            # iteration, the portion of the array that you look at
            # shrinks because the remaining items have already been
            # sorted.
            for j in range(n - i - 1):
                if food_list[j].get_expiration_date().split("/")[2] >= \
                        food_list[j + 1].get_expiration_date().split("/")[2]:
                    if food_list[j].get_expiration_date().split("/")[0] >= \
                            food_list[j + 1].get_expiration_date().split("/")[0]:
                        if food_list[j].get_expiration_date().split("/")[1] > \
                                food_list[j + 1].get_expiration_date().split("/")[1]:
                            # If the item you're looking at is greater than its
                            # adjacent value, then swap them
                            food_list[j], food_list[j + 1] = food_list[j + 1], food_list[j]

                            # Since you had to swap two elements,
                            # set the `already_sorted` flag to `False` so the
                            # algorithm doesn't finish prematurely
                            already_sorted = False

                        elif food_list[j].get_expiration_date().split("/")[1] == \
                                food_list[j + 1].get_expiration_date().split("/")[1]:
                            if sorted([food_list[j].get_name(), food_list[j + 1].get_name()])[0] \
                                    == food_list[j + 1].get_name():
                                food_list[j], food_list[j + 1] = food_list[j + 1], food_list[j]
                                already_sorted = False

            # If there were no swaps during the last iteration,
            # the array is already sorted, and you can terminate
            if already_sorted:
                break
        return food_list
