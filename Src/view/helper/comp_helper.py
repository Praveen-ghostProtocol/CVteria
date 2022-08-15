import tkinter as tk

class ComponentHelper():
    def __init__(self):
        print('component helper')

    def create_label_entry(self, grid_placeholder, row, txt, val):
        grid_placeholder.label = tk.Label(grid_placeholder, text = txt,font=('Verdana',10),bg='white',fg='black',padx=5,pady=5, anchor=tk.W)
        grid_placeholder.label.grid(row=row, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        grid_placeholder.entry = tk.Entry(grid_placeholder, width=82)
        self.change_text(grid_placeholder.entry, val)
        grid_placeholder.entry.grid(row=row, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        return grid_placeholder.entry

    def create_label_label(self, grid_placeholder, row, txt, val):
        grid_placeholder.label = tk.Label(grid_placeholder, text = txt,font=('Verdana',10),bg='white',fg='black',padx=5,pady=5, anchor=tk.W)
        grid_placeholder.label.grid(row=row, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        grid_placeholder.label2 = tk.Label(grid_placeholder, text = val,font=('Verdana',10),bg='grey',fg='black',padx=5,pady=5, anchor=tk.W, width=60)
        grid_placeholder.label2.grid(row=row, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        return grid_placeholder.label2

    def change_text(self, comp, txt):
        comp.delete(0,tk.END)
        comp.insert(0,txt)

    def create_label_options_menu(self, grid_placeholder, row, txt, vals, option_changed, default_value=''):
        grid_placeholder.label = tk.Label(grid_placeholder, text = txt,font=('Verdana',10),bg='white',fg='black',padx=5,pady=5, anchor=tk.W)
        grid_placeholder.label.grid(row=row, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # datatype of menu text
        clicked = tk.StringVar()

        clicked.set(vals[0])

        if(default_value != ''):
            clicked.set(default_value)

        grid_placeholder.optionMenu = tk.OptionMenu(grid_placeholder, clicked, *vals, command=option_changed)

        grid_placeholder.optionMenu.grid(row=row, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        return clicked, grid_placeholder.optionMenu

    def remove_all_widgets(self, win):
        for comp in win.grid_slaves():
            if int(comp.grid_info()["row"]) >= 0:
                comp.grid_forget()
        
    def add_background(self, win, img, height=0.80):
        win.img= tk.PhotoImage(file=img)

        win.canvas= tk.Canvas(win, bg='#CC8066', height=720, width=1280)
        win.canvas.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        win.canvas.create_image(1280,720,anchor=tk.SE,image=win.img)

        win.frame = tk.Frame(win.canvas, bg='#CC8066',bd=5)
        win.frame.place(relx=0.07,rely=0.02,relwidth=0.55,relheight=height)
        
        return win.frame
    
