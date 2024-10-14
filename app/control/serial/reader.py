from threading import Thread, Lock

import serial
from serial.tools import list_ports

from app.control.buffer.signal_buffer import Buffer
from app.utils.exceptions import *


class Reader():
    def __init__(
            self,
            input_: str,
            input_freq: int = 1000,
            n_entries: int = 1,
            separator: str = " ",
            selector = None
        ):
        self.__mutex = Lock()
        self.__buffers = [Buffer() for i in range(n_entries)]
        self.__values_to_send = [list() for i in range(n_entries)]
        self.__time_list = list()
        self.__times_to_send = list()
        self.__period = [0 for i in range(n_entries)]
        self.__reading = True
        self.__actualization = True

    
        self.__ser = serial.Serial(
            port=input_,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

        def __reader():
            reading = True
            step = 1 / input_freq
            time = 0
            limit = input_freq / 2

            while reading:
                try:
                    bytesWaiting = self.__ser.inWaiting()

                    if (bytesWaiting != 0):
                        try:
                            value = self.__ser.readline()
                        except:
                            if selector:
                                selector.release()

                            break

                        if value:
                            try:
                                value = value.decode("utf-8")
                                value = value.replace("\r", "")
                                value = value.replace("\n", "")
                                value = list(map(float, value.split(separator)))
                            except:
                                continue

                            if len(value) < n_entries:
                                continue
                            elif len(value) > n_entries:
                                value = value[:n_entries]

                            with self.__mutex:
                                for i in range(n_entries):
                                    self.__buffers[i].put_read(value[i])

                                self.__time_list.append(time)

                                if sum([buffer.can_send(limit) for buffer in self.__buffers]) == n_entries:
                                    self.__values_to_send = []
                                    self.__period = []
                                    
                                    for buffer in self.__buffers:
                                        sequence, period = buffer.get_sequence()
                                        self.__values_to_send.append(sequence)
                                        self.__period.append(period * step)
                                    
                                        buffer.flush()
                                        
                                    self.__times_to_send = self.__time_list
                                    self.__time_list = list()
                                    self.__actualization = True
                                    
                                reading = self.__reading

                            time += step
                except:
                    with self.__mutex:
                        self.__reading = False
                        self.__ser.close()
                    break
        
        self.thread = Thread(target=__reader, args=[])
        self.thread.daemon = True
        self.thread.start()

    def get_reading(self):
        with self.__mutex:
            if len(self.__values_to_send[0]) > 0:
                self.__actualization = False
                return self.__values_to_send, self.__times_to_send, self.__period

            else:
                return [buffer.get_sequence()[0] for buffer in self.__buffers], self.__time_list, self.__period
    
    def kill(self):
        with self.__mutex:
            self.__reading = False
    
    def is_reading(self):
        with self.__mutex:
            return self.__reading

    def has_actualization(self):
        return self.__actualization
            
    def get_ports():
        return [str(port) for port in list_ports.comports()]
