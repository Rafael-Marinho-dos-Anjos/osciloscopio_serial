import tkinter as tk
from time import sleep

from app.config.config_holder import ConfigHolder
from app.utils.safe_execute import safe_execute


class FrequenceConfig(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        self.__master = master
        self.title("Frequêcia de amostragem")
        size = (350, 150)
        self.minsize(*size)
        self.geometry(f"{size[0]}x{size[1]}")
        self.__draw_window()
        self.bind("<Return>", self.__confirm)

        self.attributes('-topmost', 1)
    
    def __draw_window(self):
        self.__text = tk.Label(
            self,
            text="Configurar frequência de amostragem."
        )
        self.__entry_text = tk.Label(
            self,
            text="Frequência: "
        )
        self.__entry_greatness = tk.Label(
            self,
            text=" Hz"
        )
        self.__freq_var = tk.StringVar(value=ConfigHolder().get_frequence())
        self.__entry = tk.Entry(
            self,
            textvariable=self.__freq_var,
            justify="right"
        )
        self.__ok_button = tk.Button(
            self,
            text="Confirmar",
            command= lambda: self.__confirm()
        )

        self.__text.place(relx=0.5, rely=0.25, anchor='center')
        self.__entry_text.place(relx=0.25, rely=0.5, anchor='e')
        self.__entry.place(relx=0.5, rely=0.5, relwidth=0.5, anchor='center')
        self.__entry_greatness.place(relx=0.75, rely=0.5, anchor='w')
        self.__ok_button.place(relx=0.5, rely=0.75, anchor='center')

    def __confirm(self, runnable=True):
        def __set_freq():
            freq = float(self.__freq_var.get())

            if freq <= 0:
                raise Exception()
            
            ConfigHolder().set_frequence(freq)

            if hasattr(self.__master, "_MainWindow__controller"):
                running = self.__master._MainWindow__controller.is_running()
                self.__master._MainWindow__controller.stop()

                sleep(1)

                if running:
                    self.__master.start()
                    
            self.destroy()
        
        safe_execute(
            __set_freq,
            "Insira um valor de frequência válido."
        )
