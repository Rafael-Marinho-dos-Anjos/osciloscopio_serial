from threading import Thread, Lock
from time import sleep

from app.control.graphics.graph_generator import GraphGenerator
from app.utils.singleton import SingletonMeta
from app.view.main_window import MainWindow


class Aplication(metaclass=SingletonMeta):
    def __init__(self):
        self.__graph_gen = GraphGenerator()
        self.__window = MainWindow()
        self.__window.bind_controller(self)

        self.__mutex = Lock()
        self.__running = False

    def execute(self):
        def __runner():
            with self.__mutex:
                running = self.__running

            while running:
                try:
                    size = self.__window.get_win_shape()
                    self.__graph_gen.config(size=size)

                    sleep(0.5)

                    img = self.__graph_gen.get_graph()
                    self.__window.update_image(img)

                    with self.__mutex:
                        running = self.__running
                
                except:
                    break
            
            self.stop()
        
        self.__graph_gen.start()

        with self.__mutex:
            self.__running = True

        self.__thread = Thread(target=__runner)
        self.__thread.start()

    def run(self):
        self.__window.init_window()

    def stop(self):
        with self.__mutex:
            self.__running = False

        self.__graph_gen.stop()
        