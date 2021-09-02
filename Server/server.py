from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from Person import Person

Host = 'localhost'
port = 5500
BUFsize = 1024
MAX_CONNECTIONS = 10
ADDR = (Host, port)

# connecting server with localhost
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

persons = []


def wait_for_conn(Server):
    while True:
        try:
            client, addr = Server.accept()
            person = Person(addr, client)
            # recieve the name of the client
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server")
            comm = Thread(target=client_communication, args=(person,))
            comm.start()

        except Exception as e:
            print(e)


def broadcast(msg, name):
    # sending messages to all clients connected
    for person in persons:
        if name == "":
            person.client_socket.send(bytes(msg, "utf8"))
        else:
            person.client_socket.send(bytes(name, "utf8") + msg)


def client_communication(person):
    client = person.client_socket
    name = client.recv(BUFsize).decode("utf8")
    person.set_name(name)

    msg = f"{name} has joined the chat!"
    broadcast(msg, "")
    while True:
        msg = client.recv(BUFsize)
        if msg == bytes("{quit}", "utf8"):
            client.close()
            persons.remove(person)
            broadcast(f"{name} has left the chat ...", "")
            print(f"[DISCONNECTED] {name} is disconnected")
            break
        else:
            broadcast(msg, name + ":")


if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTIONS)
    print("waiting for connection....")
    Accept_thread = Thread(target=wait_for_conn(SERVER))
    Accept_thread.start()
    Accept_thread.join()  # stopping the current thread until termination of the referenced thread
    SERVER.close()
