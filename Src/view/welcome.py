import tkinter as tk

class Welcome():
    def __init__(self, win):
        print('welcome constructor')
        self.createWidgets(win)

    def createWidgets(self, win):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(0, weight=1)
        win.columnconfigure(0, weight=1)

        win.python_image = tk.PhotoImage(file="./images/welcome.gif")
        label = tk.Label(win, image=win.python_image)
        label.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
