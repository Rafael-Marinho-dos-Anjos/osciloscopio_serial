from math import pi, sin
from threading import Thread, Lock

import serial
from serial.tools import list_ports

from app.control.buffer.signal_buffer import Buffer


list_ports.comports()

class Reader():
    def __init__(
            self,
            input: str,
            input_freq: int = 1000,
            n_entries: int = 1,
            separator: str = " "
        ):
        self.mutex = Lock()
        self.buffers = [Buffer() for i in range(n_entries)]
        self.values_to_send = [list() for i in range(n_entries)]
        self.time_list = list()
        self.times_to_send = list()
        self.period = [0 for i in range(n_entries)]
        self.reading = True
        self.actualization = True

    
        self.ser = serial.Serial(
            port=input,
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
                bytesWaiting = self.ser.inWaiting()

                if (bytesWaiting != 0):
                    value = self.ser.readline()

                    if value:
                        try:
                            value = value.decode("utf-8")
                            value = value.replace("\r", "")
                            value = value.replace("\n", "")
                            value = list(map(float, value.split(separator)))
                        except:
                            continue

                        if len(value) != n_entries:
                            continue

                        with self.mutex:
                            for i in range(n_entries):
                                self.buffers[i].put_read(value[i])

                            self.time_list.append(time)

                            if sum([buffer.can_send(limit) for buffer in self.buffers]) == n_entries:
                                self.values_to_send = []
                                self.period = []
                                
                                for buffer in self.buffers:
                                    sequence, period = buffer.get_sequence()
                                    self.values_to_send.append(sequence)
                                    self.period.append(period * step)
                                
                                    buffer.flush()
                                    
                                self.times_to_send = self.time_list
                                self.time_list = list()
                                self.actualization = True
                                
                            reading = self.reading

                        time += 10 * step
        
        self.thread = Thread(target=__reader, args=[])
        self.thread.start()

    def get_reading(self):
        with self.mutex:
            if len(self.values_to_send[0]) > 0:
                self.actualization = False
                return self.values_to_send, self.times_to_send, self.period

            else:
                return [buffer.get_sequence()[0] for buffer in self.buffers], self.time_list, self.period
    
    def kill(self):
        with self.mutex:
            self.reading = False

    def has_actualization(self):
        return self.actualization
            
    def get_ports():
        return [str(port) for port in list_ports.comports()]
