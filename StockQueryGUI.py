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
        self.text_resumen = None
        self.text_resultado = None
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

        self.text_resultado = Text(self, width=90, height=30, wrap=WORD)
        self.text_resultado.grid(row=4, column=0, columnspan=4)
        scrollb = Scrollbar(self, command=self.text_resultado.yview)
        scrollb.grid(row=4, column=5, sticky='nsew')
        self.text_resultado['yscrollcommand'] = scrollb.set

    def retrieve_data(self):
        self.text_resultado.delete('1.0', END)

        s = self.stringvar_input.get()
        # self.stock_controller.stocks_test_connect(s)
        self.stock_controller.stocks_test()  # linea para hcer pruebas con datos locales

        conn = self.stock_controller.stocks_test_retrieve_data()
        if conn.metadata is not None:
            self.text_resumen = Label(self, text=conn.metadata.get_metadata_data())
            self.text_resumen.grid(row=3, column=0, columnspan=4)

        sdd = conn.stock_day_data
        for i in sdd:
            self.text_resultado.insert(END, i.get_stockdaydata_data())
            self.text_resultado.insert(END, '\n')
            self.text_resultado.insert(END, '\n')

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

root.geometry("800x600")

# creation of an instance
app = Window(root)

# mainloop
root.mainloop()
