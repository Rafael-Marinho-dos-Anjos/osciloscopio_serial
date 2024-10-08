from math import pi, sin
from threading import Thread, Lock

import serial
from serial.tools import list_ports

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
        self.read_values = [list() for i in range(n_entries)]
        self.values_to_send = [list() for i in range(n_entries)]
        self.time_list = list()
        self.times_to_send = list()
        self.period = [0 for i in range(n_entries)]
        self.reading = True
        self.actualization = True

        if input.upper() == "GENERATOR":
            def __reader():
                reading = True
                freq = 2*pi*60 # angular frequence
                step = 1 / input_freq
                time = 0
                period_count = 0

                while reading:
                    value = sin(freq * time)
                    period_count += 1

                    if len(self.read_values[0]) > 0 and self.read_values[0][-1] < 0 and value >= 0:
                        with self.mutex:
                            self.period[0] = period_count * step
                            self.values_to_send = self.read_values
                            self.times_to_send = self.time_list
                            self.read_values[0] = list()
                            self.time_list = list()
                            period_count = 0

                    with self.mutex:
                        self.read_values[0].append(value)
                        self.time_list.append(time)

                    time += step
                
                    with self.mutex:
                        reading = self.reading

        else:
            self.ser = serial.Serial(
                port=input,
                baudrate=9600,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.SEVENBITS
            )

            def __reader():
                zero_passage = [False for i in range(n_entries)]
                period_count = [0 for i in range(n_entries)]
                reading = True
                step = 1 / input_freq
                time = 0
                avg_signal = [0 for i in range(n_entries)]
                not_actualizated = True

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
                                    period_count[i] += 1

                                    if len(self.read_values[i]) > 0 and self.read_values[i][-1] < avg_signal[i] and value[i] >= avg_signal[i]:
                                        self.period[i] = period_count[i] * step
                                        zero_passage[i] = zero_passage[i] + 1 if zero_passage[i] < 2 else 2
                                        period_count[i] = 0

                                    self.read_values[i].append(value[i])

                                self.time_list.append(time)

                                if sum(zero_passage) == 2 * n_entries:
                                    self.values_to_send = self.read_values
                                    self.read_values = [list() for i in range(n_entries)]
                                    zero_passage = [False for i in range(n_entries)]
                                    self.times_to_send = self.time_list
                                    self.time_list = list()
                                    self.actualization = True
                                    not_actualizated = False
                                    avg_signal = [
                                        sum(self.values_to_send[i]) / len(self.times_to_send)
                                        for i in range(n_entries)]

                                if not_actualizated:
                                    avg_signal = [
                                        sum(self.read_values[i]) / len(self.time_list)
                                        for i in range(n_entries)]

                            time += step
                            reading = self.reading
        
        self.thread = Thread(target=__reader, args=[])
        self.thread.start()

    def get_reading(self):
        with self.mutex:
            if len(self.values_to_send[0]) > 0:
                self.actualization = False
                return self.values_to_send, self.times_to_send, self.period

            else:
                return self.read_values, self.time_list, self.period
    
    def kill(self):
        with self.mutex:
            self.reading = False

    def has_actualization(self):
        return self.actualization
            
    def get_ports():
        return [str(port) for port in list_ports.comports()]
