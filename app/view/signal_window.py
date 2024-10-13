import tkinter as tk
from time import sleep

from app.config.config_holder import ConfigHolder
from app.utils.safe_execute import safe_execute


class SignalConfig(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        self.__master = master
        self.title("Configurar Sinais")
        size = (350, 200)
        self.minsize(*size)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(0, 0)

        self.__signal_labels = ConfigHolder().get_signal_labels()
        self.__draw_window()
        self.bind("<Return>", self.__confirm)

        self.attributes('-topmost', 1)
    
    def __draw_window(self):
        self.__n_text = tk.Label(
            self,
            text="Número de sinais: "
        )
        self.__n = tk.IntVar(value=len(self.__signal_labels))
        self.__n_entry = tk.Entry(
            self,
            textvariable=self.__n
        )

        self.__selector_label = tk.Label(
            self,
            text="Sinal: "
        )
        self.__selected = tk.StringVar(value=self.__signal_labels[0])
        self.__signal_selector = tk.OptionMenu(
            self,
            self.__selected,
            *self.__signal_labels
            )
        self.__signal_selector.bind("<Button-1>", self.__update_labels)

        self.__label_signal = tk.Label(self, text="Label: ")
        self.__label = tk.StringVar(value=self.__signal_labels[0])
        self.__entry_label = tk.Entry(self, textvariable=self.__label)
        self.__update_labels()
        
        self.__ok_button = tk.Button(
            self,
            text="Confirmar",
            command= lambda: self.__confirm()
        )

        self.__n_text.place(relx=0.33, rely=0.15, anchor='e')
        self.__n_entry.place(relx=0.33, rely=0.15, anchor='w')
        self.__selector_label.place(relx=0.33, rely=0.4, anchor='e')
        self.__signal_selector.place(relx=0.33, rely=0.4, anchor='w')
        self.__label_signal.place(relx=0.33, rely=0.6, anchor='e')
        self.__entry_label.place(relx=0.33, rely=0.6, anchor='w')
        self.__ok_button.place(relx=0.5, rely=0.8, anchor='center')

    def __update_labels(self, runnable = True):
        n = [0]
        
        def __get_n(n_):
            n_[0] = int(self.__n.get())

            if n_[0] <= 0:
                n_[0] = 0
                Exception()

        safe_execute(
            lambda: __get_n(n),
            "Insira um número de sinais válido."
        )

        n = n[0]

        if n == 0:
            return False

        elif n > 8:
            safe_execute(
                lambda: 1/0,
                "No máximo 8 sinais simultâneos são permitidos."
            )
            return False
        
        selected = self.__selected.get()

        try:
            sel_index = self.__signal_labels.index(selected)
            self.__signal_labels[sel_index] = self.__label.get()
            
        except:
            pass

        if len(self.__signal_labels) > n:
            self.__signal_labels = self.__signal_labels[:n]

        elif len(self.__signal_labels) < n:
            for i in range(len(self.__signal_labels), n):
                self.__signal_labels.append("ABCDEFGH"[i])
        
        self.__signal_selector.children["menu"].delete(0, 'end')

        def __select(s):
            def __func():
                self.__update_labels()

                self.__selected.set(s)
                self.__label.set(s)
                
            return __func

        for label in self.__signal_labels:
            self.__signal_selector.children["menu"].add_command(
                label=label,
                command=__select(label))

        self.__selected.set(selected)
        
        return True

    def __confirm(self, runnable=True):
        def __setting_labels():
            if not self.__update_labels():
                return
            
            ConfigHolder().set_num_signals(len(self.__signal_labels))

            for i, label in enumerate(self.__signal_labels):
                ConfigHolder().config_signal_label(i, label)
            
            self.destroy()

            if hasattr(self.__master, "_MainWindow__controller"):
                running = self.__master._MainWindow__controller.is_running()
                self.__master._MainWindow__controller.stop()

                sleep(1)

                if running:
                    self.__master.start()

        
        safe_execute(lambda: __setting_labels())
