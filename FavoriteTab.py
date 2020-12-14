from tkinter import ttk

from FoodFrame import FoodFrame


class FavoriteTab:
    def __init__(self, notebook, application, image):
        self.application = application
        tab_frames_style = ttk.Style()
        tab_frames_style.configure('TFrame', background='snow2')
        self.tab_frame = ttk.Frame()
        self.frames = []
        self.image = image
        self.notebook = notebook
        notebook.add(self.tab_frame, image=image)
        self.expired_tab = None

    def set_expired_tab(self, expired_tab):
        self.expired_tab = expired_tab

    def add_food(self, food, category):
        new_frame = FoodFrame(self.tab_frame, food, category, self, self.expired_tab, self.application, False)
        self.frames.append(new_frame)

    def get_tab_frame(self):
        return self.tab_frame

    def add_frame(self, frame):
        self.frames.append(frame)

    def get_frames(self):
        return self.frames

    def delete_frame(self, food):
        for frame in self.frames:
            if frame.get_food() == food:
                frame.get_sub_master().destroy()


