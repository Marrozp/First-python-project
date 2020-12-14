

class Food:

    def __init__(self, name, expiration_date, favorite):
        self.name = name
        self.expiration_date = expiration_date
        self.favorite = favorite
        self.is_expired = False

    def is_favorite(self):
        return self.favorite

    def set_favorite(self, data):
        self.favorite = data

    def set_as_expired(self):
        self.is_expired = True

    def already_expired(self):
        return self.is_expired

    def get_name(self):
        return self.name

    def get_expiration_date(self):
        return self.expiration_date
