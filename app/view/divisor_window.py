import tkinter as tk
from time import sleep

from app.config.config_holder import ConfigHolder
from app.utils.safe_execute import safe_execute


class DivisorConfig(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        self.__master = master
        self.title("Divisor de tensão")
        size = (350, 150)
        self.minsize(*size)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(0, 0)
        self.__draw_window()
        self.bind("<Return>", self.__confirm)

        self.attributes('-topmost', 1)
    
    def __draw_window(self):
        self.__text = tk.Label(
            self,
            text="Configurar divisor de tensão."
        )

        self.__enabled = tk.IntVar(value=ConfigHolder().divisor_is_enabled())
        self.__checkbutton = tk.Checkbutton(
            self,
            text="Ativar Divisor de Tensão",
            variable=self.__enabled, 
            onvalue=1, offvalue=0,
            command=self.__toggle_checkbutton
        )

        self.__entry_text_rb = tk.Label(
            self,
            text="Rb: "
        )
        self.__entry_greatness_rb = tk.Label(
            self,
            text=" Ohms"
        )

        rb, rc = ConfigHolder().get_divisor_resistors()
        self.__rb_var = tk.StringVar(value=rb)
        self.__entry_rb = tk.Entry(
            self,
            textvariable=self.__rb_var,
            justify="right"
        )

        self.__entry_text_rc = tk.Label(
            self,
            text="Rc: "
        )
        self.__entry_greatness_rc = tk.Label(
            self,
            text=" Ohms"
        )
        self.__rc_var = tk.StringVar(value=rc)
        self.__entry_rc = tk.Entry(
            self,
            textvariable=self.__rc_var,
            justify="right"
        )
        self.__ok_button = tk.Button(
            self,
            text="Confirmar",
            command= lambda: self.__confirm()
        )

        self.__text.place(relx=0.5, rely=0.15, anchor='center')
        self.__checkbutton.place(relx=0.5, rely=0.35, anchor='center')
        self.__entry_text_rb.place(relx=0.25, rely=0.5, anchor='e')
        self.__entry_rb.place(relx=0.5, rely=0.5, relwidth=0.5, anchor='center')
        self.__entry_greatness_rb.place(relx=0.75, rely=0.5, anchor='w')
        self.__entry_text_rc.place(relx=0.25, rely=0.65, anchor='e')
        self.__entry_rc.place(relx=0.5, rely=0.65, relwidth=0.5, anchor='center')
        self.__entry_greatness_rc.place(relx=0.75, rely=0.65, anchor='w')
        self.__ok_button.place(relx=0.5, rely=0.8, anchor='center')

    def __toggle_checkbutton(self):
        if self.__enabled.get():
            self.__entry_rb.config(state="normal")
            self.__entry_rc.config(state="normal")
        else:
            self.__entry_rb.config(state="disabled")
            self.__entry_rc.config(state="disabled")


    def __confirm(self, runnable=True):
        def __set_divisor():
            rb = float(self.__entry_rb.get())
            rc = float(self.__entry_rc.get())

            if rb <= 0 or rc <= 0:
                raise Exception()
            
            ConfigHolder().enable_divisor(self.__enabled.get())
            ConfigHolder().set_divisor_resistors(rb, rc)
                    
            self.destroy()

            if hasattr(self.__master, "_MainWindow__controller"):
                running = self.__master._MainWindow__controller.is_running()
                self.__master._MainWindow__controller.stop()

                sleep(1)

                if running:
                    self.__master.start()
        
        safe_execute(
            __set_divisor,
            "Insira valores de resistores válidos."
        )
