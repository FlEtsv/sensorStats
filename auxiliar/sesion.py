# sesion.py
import threading


class sesion:
    __instance = None
    __lock = threading.Lock()
    vin = None
    ip_port = None
    coordenadas = None

    @staticmethod
    def get_instance():
        if sesion.__instance is None:
            sesion()
        return sesion.__instance

    def __init__(self):
        if sesion.__instance is not None:
            raise Exception("Esta clase es un singleton!")
        else:
            sesion.__instance = self

    def set_vin(self, vin):
        self.vin = vin

    def get_vin(self) -> str:
        return self.vin

    def set_ip_port(self, ip_port):
        self.ip_port = ip_port

    def get_ip_port(self) -> str:
        return self.ip_port

    def clear(self):
        self.vin = ''
        self.ip_port = ''

    def set_coordenadas(self, coordenadas):
        self.coordenadas = coordenadas

    def get_coordenadas(self):
        return self.coordenadas