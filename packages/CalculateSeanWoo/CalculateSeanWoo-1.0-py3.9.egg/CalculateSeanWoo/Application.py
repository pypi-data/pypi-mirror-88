from tkinter import *
from .Window import Window

class Application:
    def __init__(self):
        self._window = None

    def InitializeComponent(self):
        self._window = Window()
        self._window.setSize(500, 200)
        self.root = self._window
        self.root.configure(bg="black")

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.columnconfigure(0, weight=1)   
        self.root.columnconfigure(1, weight=2)   
        self.root.columnconfigure(2, weight=1)   
        self.root.columnconfigure(2, weight=1)   

        self.entry = Entry(self.root, width=70)
        self.entry.grid(column=0, row=0, columnspan=6)

        self.delete = Button(self.root, text="C", width=15)
        self.delete.grid(column=0, row=1)

        self.openBracket = Button(self.root, text="(", width=15)
        self.openBracket.grid(column=1, row=1)

        self.closeBracket = Button(self.root, text=")", width=15)
        self.closeBracket.grid(column=2, row=1)

        self.b1 = Button(self.root, text="1", width=15)
        self.b1.grid(column=0, row=2)

        self.b2 = Button(self.root, text="2", width=15)
        self.b2.grid(column=1, row=2)

        self.b3 = Button(self.root, text="3", width=15)
        self.b3.grid(column=2, row=2)

        self.b4 = Button(self.root, text="4", width=15)
        self.b4.grid(column=0, row=3)

        self.b5 = Button(self.root, text="5", width=15)
        self.b5.grid(column=1, row=3)

        self.b6 = Button(self.root, text="6", width=15)
        self.b6.grid(column=2, row=3)

        self.b7 = Button(self.root, text="7", width=15)
        self.b7.grid(column=0, row=4)

        self.b8 = Button(self.root, text="8", width=15)
        self.b8.grid(column=1, row=4)

        self.b9 = Button(self.root, text="9", width=15)
        self.b9.grid(column=2, row=4)

        self.b0 = Button(self.root, text="0", width=15)
        self.b0.grid(column=1, row=5)
        
        self.add = Button(self.root, text="+", width=15)
        self.add.grid(column=3, row=2)

        self.sub = Button(self.root, text="-", width=15)
        self.sub.grid(column=3, row=3)

        self.mul = Button(self.root, text="*", width=15)
        self.mul.grid(column=3, row=4)

        self.div = Button(self.root, text="/", width=15)
        self.div.grid(column=3, row=5)

        self.answer = Button(self.root, text="=", width=15)
        self.answer.grid(column=2, row=5)

        self.tch = Button(self.root, text=".", width=15)
        self.tch.grid(column=0, row=5)

    def EndInit(self):
        self._window.show()
        
