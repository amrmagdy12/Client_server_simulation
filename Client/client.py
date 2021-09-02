import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock


class client:
    Host = 'localhost'
    port = 5500
    BUFsize = 512
    ADDR = (Host, port)

    def __init__(self, name):
        self.name = name
        self.client_id = socket(AF_INET, SOCK_STREAM)
        self.client_id.connect(self.ADDR)
        self.messages = []
        recievethread = Thread(target=self.recv_message)
        recievethread.start()
        self.client_id.send(bytes(name, 'utf8'))
        self.lock = Lock()

    def send_message(self, msg):
        try:
            self.client_id.send(bytes(msg, "utf8"))
        except Exception as e:
            self.client_id = socket(AF_INET, SOCK_STREAM)
            self.client_id.connect(self.ADDR)
            print(e)

    def recv_message(self):
        # receive messages from server
        while True:
            try:
                msg = self.client_id.recv(self.BUFsize).decode("utf8")
                # in case the server-client socket closed so stop receiving from server
                if msg == "":
                    self.client_id.close()
                    break

                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def __repr__(self):
        return f"client({self.name} , {self.client_id})"

    def get_messages(self):
        messages_copy = self.messages[:]

        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")
