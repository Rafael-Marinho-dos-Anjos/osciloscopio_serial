from threading import Lock

from app.control.serial.reader import Reader
from app.utils.exceptions import *
from app.utils.singleton import SingletonMeta


class PortSelector(metaclass=SingletonMeta):
    def __init__(self):
        self.__selected = False
        self.__mutex = Lock()
    
    def get_available_ports():
        return Reader.get_ports()
    
    def select(self, port):
        def __define_port(p):
            if p in PortSelector.get_available_ports():
                with self.__mutex:
                    self.__port = p
                    self.__selected = True
            else:
                raise InvalidSerialDeviceException("Dispositivo informado não está conectado")

        if not hasattr(self, "_PortSelector__port"):
            __define_port(port)
        else:
            with self.__mutex:
                if self.__port in PortSelector.get_available_ports():
                    raise DeviceAlreadySelectedException("Já existe uma porta selecionada")
                else:
                    __define_port(port)

    def get_port(self):
        with self.__mutex:
            if not hasattr(self, "_PortSelector__port") or not self.__selected:
                raise PortNotSelectedException("Dispositivo serial não selecionado")
            
            return self.__port

    def release(self):
        if hasattr(self, "_PortSelector__port"):
            with self.__mutex:
                del self.__port
                self.__selected = False

    def ready(self):
        with self.__mutex:
            return self.__selected
