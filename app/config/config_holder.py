import json
from os.path import exists

from app.utils.singleton import SingletonMeta


class ConfigHolder(metaclass=SingletonMeta):
    def __init__(self):
        self.__cfg_file_path = "app/config/cfg.json"

        if exists(self.__cfg_file_path):
            with open(self.__cfg_file_path) as cfg:
                self.__cfg_dict = json.loads(cfg.read())
        
        if not hasattr(self, "_ConfigHolder__cfg_dict"):
            self.__cfg_dict = {
                "frequence": 1000.0,
                "signals": ["A"],
                "divisor": {
                    "enabled": False,
                    "Rb": 100.0,
                    "Rc": 100.0
                }
            }

        else:
            if "frequence" not in self.__cfg_dict.keys():
                self.__cfg_dict["frequence"] = 1000

            if "signals" not in self.__cfg_dict.keys():
                self.__cfg_dict["signals"] = ["A"]
            

            if "divisor" not in self.__cfg_dict.keys():
                self.__cfg_dict["divisor"] = {
                    "enabled": False,
                    "Rb": 100.0,
                    "Rc": 100.0
                }            

    def set_frequence(self, frequence: float):
        self.__cfg_dict["frequence"] = frequence

    def get_frequence(self):
        return self.__cfg_dict["frequence"]

    def set_num_signals(self, n: int):
        if len(self.__cfg_dict["signals"]) > n:
            self.__cfg_dict["signals"] = self.__cfg_dict["signals"][:n]

        elif len(self.__cfg_dict["signals"]) < n:
            for i in range(len(self.__cfg_dict["signals"]) - n):
                self.__cfg_dict["signals"].append(
                    "ABCDEFGH"[n + i]
                )

    def config_signal_label(self, index: str, label: str):
        self.__cfg_dict["signals"][index] = str(label)
    
    def get_signal_labels(self):
        return self.__cfg_dict["signals"]

    def enable_divisor(self, enable: bool):
        self.__cfg_dict["divisor"]["enabled"] = enable
    
    def set_divisor_resistors(self, rb: float, rc: float):
        self.__cfg_dict["divisor"]["Rb"] = rb
        self.__cfg_dict["divisor"]["Rc"] = rc
    
    def divisor_is_enabled(self):
        return self.__cfg_dict["divisor"]["enabled"]
    
    def get_divisor_resistors(self):
        return self.__cfg_dict["divisor"]["Rb"], self.__cfg_dict["divisor"]["Rc"]

    def save(self):
        with open(self.__cfg_file_path, "w") as file:
            json.dump(self.__cfg_dict, file)
