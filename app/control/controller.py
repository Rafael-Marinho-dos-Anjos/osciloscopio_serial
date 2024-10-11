from app.control.graphics.graph_generator import GraphGenerator
from app.control.serial.serial_port import PortSelector
from app.utils.singleton import SingletonMeta


class Aplication(metaclass=SingletonMeta):
    def __init__(self):
        self.__port_selector = PortSelector()
        self.__graph_gen = GraphGenerator()

    