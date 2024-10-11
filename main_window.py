import tkinter as tk
from threading import Thread, Lock

from app.control.graphics.graph_generator import GraphGenerator
from app.control.serial.serial_port import PortSelector
from app.utils.singleton import SingletonMeta


def donothing():
    pass

class MainWindow(metaclass=SingletonMeta):
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.minsize(720, 360)
        self.__root.title("Osciloscópio Serial")

        self.__graph_gen = GraphGenerator()
        self.__port_selector = PortSelector()

        self.__running = False
        self.__mutex = Lock()

        self.__create_menu_bar()
    
    def start(self):
        self.__root.mainloop()
    
    def __create_menu_bar(self):
        self.__menubar = tk.Menu(self.__root)
        self.__root.config(menu=self.__menubar)

        self.__conf_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__conf_menu.add_command(label="Frequência de amostragem", command=self.__config_frequence)
        self.__conf_menu.add_command(label="Entrada de sinais", command=self.__signals)
        self.__menubar.add_cascade(label="Config", menu=self.__conf_menu)

        self.__ports_menu = tk.Menu(self.__menubar, tearoff=0, postcommand=self.__update_ports_menu)
        self.__select_port_submenu = tk.Menu(self.__ports_menu, tearoff=0)
        # self.__ports_menu.bind("<Enter>", lambda: self.__update_ports_menu())
        self.__ports_menu.add_cascade(label="Selecionar dispositivo de entrada", menu=self.__select_port_submenu)
        self.__menubar.add_cascade(label="Portas", menu=self.__ports_menu)

    def __config_frequence(self):
        pass

    def __signals(self):
        pass

    def __update_ports_menu(self):
        ports = PortSelector.get_available_ports()

        def __create_select_command(p):
            def __select_port():
                self.__port_selector.select(p)

            return __select_port
        
        self.__select_port_submenu.delete(0, 'end')

        for port in ports:
            if self.__port_selector.ready() and self.__port_selector.get_port() == port:
                self.__select_port_submenu.add_command(label="-> "+port)
            else:
                self.__select_port_submenu.add_command(label="   "+port, command=__create_select_command(port))

if __name__ == "__main__":
    MainWindow().start()