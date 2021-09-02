class Person:
    def __init__(self, addr, client_socket):
        self.addr = addr
        self.client_socket = client_socket
        self.name = ""

    def set_name(self, name):
        self.name = name
