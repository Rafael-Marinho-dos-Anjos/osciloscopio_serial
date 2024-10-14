import tkinter as tk
from PIL.Image import fromarray
from PIL import ImageTk

from app.control.graphics.graph_generator import GraphGenerator
from app.control.serial.serial_port import PortSelector
from app.utils.singleton import SingletonMeta
from app.utils.safe_execute import safe_execute
from app.view.freq_window import FrequenceConfig
from app.view.signal_window import SignalConfig
from app.view.divisor_window import DivisorConfig
from app.config.config_holder import ConfigHolder


def donothing():
    pass

class MainWindow(metaclass=SingletonMeta):
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.minsize(720, 360)
        self.__root.title("Osciloscópio Serial")

        self.__graph_gen = GraphGenerator()
        self.__port_selector = PortSelector()

        self.__canvas = tk.Label(self.__root)
        self.__canvas.place(
            relx=0.5,
            rely=0.5,
            relwidth=0.98,
            relheight=0.98,
            anchor='center')

        self.update_image(self.__graph_gen.get_graph())
        self.__create_menu_bar()

        self.__root.protocol("WM_DELETE_WINDOW", lambda: self.__quit())
    
    def bind_controller(self, controller):
        self.__controller = controller
    
    def init_window(self):
        self.__root.mainloop()

    def __create_menu_bar(self):
        self.__menubar = tk.Menu(self.__root)
        self.__root.config(menu=self.__menubar)

        self.__conf_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__conf_menu.add_command(label="Frequência de amostragem", command=self.__config_frequence)
        self.__conf_menu.add_command(label="Entrada de sinais", command=self.__signals)
        self.__conf_menu.add_command(label="Divisor de tensão", command=self.__config_divisor)
        self.__menubar.add_cascade(label="Config", menu=self.__conf_menu)

        self.__ports_menu = tk.Menu(self.__menubar, tearoff=0, postcommand=self.__update_ports_menu)
        self.__select_port_submenu = tk.Menu(self.__ports_menu, tearoff=0)
        self.__ports_menu.add_cascade(label="Selecionar dispositivo de entrada", menu=self.__select_port_submenu)
        self.__menubar.add_cascade(label="Portas", menu=self.__ports_menu)

    def __config_frequence(self):
        frequence_config = FrequenceConfig(master=self)
        frequence_config.mainloop()

    def __signals(self):
        signal_config = SignalConfig(master=self)
        signal_config.mainloop()

    def __config_divisor(self):
        divisor_config = DivisorConfig(master=self)
        divisor_config.mainloop()

    def __update_ports_menu(self):
        ports = PortSelector.get_available_ports()

        def __create_select_command(p):
            def __select_port():
                safe_execute(
                    lambda: self.__port_selector.select(p)
                )
                self.start()

            return __select_port
        
        def __unselect_port():
            safe_execute(
                lambda: self.__port_selector.release()
            )
            self.__controller.stop()
        
        self.__select_port_submenu.delete(0, 'end')

        for port in ports:
            if self.__port_selector.ready() and self.__port_selector.get_port() == port:
                self.__select_port_submenu.add_command(label="-> "+port, command=lambda: __unselect_port())
            else:
                self.__select_port_submenu.add_command(label="   "+port, command=__create_select_command(port))

    def update_image(self, img):
        if self.__root.winfo_exists():
            img = fromarray(img)
            img = ImageTk.PhotoImage(img)

            self.__canvas.configure(image=img)
            self.__canvas.image=img

    def get_win_shape(self):
        w = self.__root.winfo_width() / 100
        h = self.__root.winfo_height() / 100

        return w, h

    def start(self):
        safe_execute(
            lambda: self.__controller.execute()
        )
    
    def __quit(self):
        self.__port_selector.release()
        self.__controller.stop()

        self.__root.destroy()
        ConfigHolder().save()
