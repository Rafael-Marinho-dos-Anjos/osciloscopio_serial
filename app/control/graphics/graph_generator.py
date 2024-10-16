import matplotlib.pyplot as plt
from time import sleep
import numpy as np
import cv2
from threading import Thread, Lock
import re

from app.control.serial.reader import Reader
from app.control.serial.serial_port import PortSelector
from app.utils.exceptions import *
from app.config.config_holder import ConfigHolder
from app.utils.singleton import SingletonMeta


class GraphGenerator(metaclass=SingletonMeta):
    def __init__(self):
        self.__port_selector = PortSelector()
        self.__signals = ConfigHolder().get_signal_labels()
        self.__size = (12, 5)
        self.__mutex = Lock()
        self.__img = None
        self.__running = False
        self.__delay = 1 / 2
        self.__reader_thread = None

    def start(self):
        if self.__running:
            return
        
        if not self.__port_selector.ready():
            raise PortNotSelectedException("Dispositivo serial não selecionado")

        port = self.__port_selector.get_port()
        self.__reader = Reader(
            port.split(" ")[0],
            n_entries=len(self.__signals),
            input_freq=ConfigHolder().get_frequence(),
            selector=self.__port_selector)
        
        enable_divisor = ConfigHolder().divisor_is_enabled()
        rb, rc = ConfigHolder().get_divisor_resistors()

        def __divisor(value):
            v = value * (rb + rc) / rb
            v += 2.5
            
            return v

        def __gen_graph():
            plt.switch_backend('agg')
            fig, ax = plt.subplots(figsize=self.__size)

            running = True
            with self.__mutex:
                delay = self.__delay

            while running:
                fig.set_size_inches(*list(map(int, self.__size)))
                sleep(delay)

                with self.__mutex:
                    if not self.__reader.has_actualization():
                        continue
                    if not self.__reader.is_reading():
                        self.__port_selector.release()
                        break

                    values, time, periods = self.__reader.get_reading()

                if len(values[0]) == 0:
                    continue

                elif len(values) > len(self.__signals):
                    values = values[:len(self.__signals)]

                ax.clear()

                for val in values:
                    if enable_divisor:
                        val = list(map(__divisor, val))

                    ax.plot(time, val)
                
                values = np.array(values)
                changes = [list() for i in range(values.shape[0])]
                val_pp = [np.max(v) - np.min(v) for v in values]
                zero_passage = values > np.mean(values, axis=0)

                for i in range(zero_passage.shape[1] - 1):
                    for j in range(zero_passage.shape[0]):
                        if zero_passage[j][i] != zero_passage[j][i+1]:
                            changes[j].append(i)
                
                val_rms = list()
                for s, change in enumerate(changes):
                    if len(change) < 3:
                        rms = values[s, :]
                    else:
                        rms = values[s, change[0]: change[2]]
                    
                    rms = np.power(rms, 2)
                    rms = np.sqrt(np.mean(rms))

                    val_rms.append(rms)

                per = [f"{1 / i :.2f}" if i > 0 else "NA" for i in periods]

                with self.__mutex:
                    ax.legend([f"Signal {self.__signals[i]}: {per[i]}Hz" for i in range(len(values))])

                    label = [f"Signal {self.__signals[i]}:\nVrms: {val_rms[i]:.2f}V\nVpp: {val_pp[i]:.2f}V" for i in range(len(values))]
                
                label = "\n\n".join(label)
                ax.set_ylabel(label)
                ax.yaxis.label.set(rotation='horizontal', ha='right')

                fig.canvas.draw()

                ncols, nrows = fig.canvas.get_width_height()
                image = np.frombuffer(
                    np.delete(fig.canvas.buffer_rgba(), -1, -1),
                    dtype=np.uint8).reshape(nrows, ncols, 3)
                
                with self.__mutex:
                    self.__img = cv2.resize(image, list(map(lambda x: int(x*100), self.__size)))
                    running = self.__running
                    delay = self.__delay

            with self.__mutex:
                self.__reader.kill()
                self.__running = False
                
                del self.__reader

        with self.__mutex:
            self.__reader_thread = Thread(target=__gen_graph)
            self.__running = True
            self.__reader_thread.daemon = True
            self.__reader_thread.start()

    def stop(self):
        with self.__mutex:
            self.__img = None
            self.__running = False

    def get_graph(self):
        with self.__mutex:
            if self.__running and self.__img is not None:
                return self.__img
        
            img = cv2.imread("image/device_nc.png")
            img = cv2.resize(img, list(map(lambda x: int(x*100), self.__size)))

            return img
    
    def config(self, **kwargs):
        if "frequence" in kwargs.keys():
            freq = kwargs["frequence"]

            if freq <= 0:
                raise InvalidUpdatingFrequenceException("Valor de frequência inválido")
            
            with self.__mutex:
                self.__delay = 1 / freq
        
        if "n_signals" in kwargs.keys():
            entries = kwargs["n_signals"]

            if entries <= 0:
                raise InvalidEntrySizeException("Número de sinais inválido")
            
            with self.__mutex:
                self.__n_entries = entries
        
        if "size" in kwargs.keys():
            size = kwargs["size"]

            if isinstance(size, str) and re.match("^\d+x\d+$", size):
                size = list(map(lambda x: float(x) / 100, size.split("x")))
            elif not (isinstance(size, tuple) or isinstance(size, list)):
                raise InvalidSizeException("A resolução informada deve ser do tipo 'wxh', tupla ou lista")

            with self.__mutex:
                self.__size = size
        

if __name__ == "__main__":
    gg = GraphGenerator()
    gg.config(size="200x100")
    cv2.imshow("", gg.get_graph())
    cv2.waitKey(0)
