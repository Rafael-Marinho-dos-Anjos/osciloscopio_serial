from app.reader import Reader
from app.utils.exceptions import *


class PortSelector:
    def __init__(self):
        self.__selected = False
    
    def get_available_ports():
        return Reader.get_ports()
    
    def select(self, port):
        def __define_port(p):
            if p in self.get_available_ports():
                self.__port = p
                self.__selected = True
            else:
                raise InvalidSerialDeviceException("Dispositivo informado não está conectado")

        if not hasattr(self, "_PortSelector__port"):
            __define_port(port)
        else:
            if self.__port in self.get_available_ports():
                raise DeviceAlreadySelectedException("Já existe uma porta selecionada")
            else:
                __define_port(port)

    def get_port(self):
        if not hasattr(self, "_PortSelector__port") or not self.__selected:
            raise PortNotSelectedException("Dispositivo serial não selecionado")
        
        return self.__port

    def release(self):
        if hasattr("_PortSelector__port"):
            del self.__port

    def ready(self):
        return self.__selected
