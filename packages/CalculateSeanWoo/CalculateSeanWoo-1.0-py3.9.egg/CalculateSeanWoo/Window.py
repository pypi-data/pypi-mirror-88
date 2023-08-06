from tkinter import *

class Window(Tk):
    def __init__(self, **args):
        self.title = "Main Window"
        self.width = 400
        self.height = 400
        super().__init__()
        super().title(self.title)
        super().geometry("400x400")

    def setSize(self, width, height):
        self.width = width
        self.height = height
        super().geometry(f"{self.width}x{self.height}")

    def show(self):
        super().mainloop()