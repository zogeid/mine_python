# Simple enough, just import everything from tkinter.
from tkinter import *
# download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
from PIL import Image, ImageTk
from StockController import *


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.stock_controller = StockController()
        self.stringvar_input = StringVar()
        self.resultado = None
        self.init_window()

    def init_window(self):
        self.master.title("Query stocks")
        self.grid()

        # BUTTONS
        label = Label(self, text="Empresa:")
        label.grid(row=0, column=0)
        entry = Entry(self, textvariable=self.stringvar_input)
        entry.grid(row=0, column=1)
        self.stringvar_input.set("ADS.DE")

        query_button = Button(self, text="Retrieve data", command=self.retrieve_data)
        query_button.grid(row=0, column=2)

        quit_button = Button(self, text="Plot", command=self.stock_controller.stocks_test_plot)
        quit_button.grid(row=0, column=3)

        self.resultado = Text(self, width=45, height=10, wrap=WORD)
        self.resultado.grid(row=3, column=0, columnspan=4)
        scrollb = Scrollbar(self, command=self.resultado.yview)
        scrollb.grid(row=3, column=5, sticky='nsew')
        self.resultado['yscrollcommand'] = scrollb.set

    def retrieve_data(self):
        s = self.stringvar_input.get()
        self.stock_controller.stocks_test_connect(s)
        conn = self.stock_controller.stocks_test_retrieve_data()
        sdd = conn.stock_day_data
        for i in sdd:
            self.resultado.insert(END, i.get_stockdaydata_data())

    def show_img(self):
        load = Image.open("chat.png")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def show_text(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()

    @staticmethod
    def client_exit():
        exit()


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("400x300")

# creation of an instance
app = Window(root)

# mainloop
root.mainloop()
