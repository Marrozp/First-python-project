from tkinter import ttk

from FoodFrame import FoodFrame


class ExpiredTab:
    def __init__(self, notebook, application, image, favorite_tab):
        self.application = application
        tab_frames_style = ttk.Style()
        tab_frames_style.configure('TFrame', background='snow2')
        self.tab_frame = ttk.Frame()
        self.frames = []
        self.image = image
        self.notebook = notebook
        self.favorite_tab = favorite_tab
        notebook.add(self.tab_frame, image=image)

    def add_food(self, food, category):
        new_frame = FoodFrame(self.tab_frame, food, category, self.favorite_tab, self, self.application, False)
        self.frames.append(new_frame)

    def get_tab_frame(self):
        return self.tab_frame

    def get_frames(self):
        return self.frames

    def delete_frame(self, food):
        for frame in self.frames:
            if frame.get_food() == food:
                frame.get_sub_master().destroy()
