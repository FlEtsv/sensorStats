class session:
    __instance = None
    vin = ''
    ip_port = ''

    def __init__(self, vin='', ip_port=''):
        if session.__instance is not None:
            raise Exception("Esta clase es un singleton!")
        else:
            self.vin = vin
            self.ip_port = ip_port
            session.__instance = self

    @staticmethod
    def get_instance():
        if session.__instance is None:
            session()
        return session.__instance

    def set_vin(self, vin):
        self.vin = vin

    def get_vin(self):
        return self.vin

    def set_ip_port(self, ip_port):
        self.ip_port = ip_port

    def get_ip_port(self):
        return self.ip_port

    def clear(self):
        self.vin = ''
        self.ip_port = ''