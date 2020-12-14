

class Category:
    def __init__(self, name, previous=None):
        self.name = name
        self.foods_list = []
        self.previous = previous

    def get_foods(self):
        return self.foods_list

    def add_food(self, food):
        self.foods_list.append(food)

    def get_name(self):
        return self.name

    def set_foods_list(self, list):
        self.foods_list = list

    def get_previous_category(self):
        return self.previous
